from .utils import checkbytes
import re

class Dictionary:
	__slots__ = ('_ct', '_tc', 'lowrange', 'ctrltable')

	def __init__(self, file, lowrange=None, ctrltable=None):
		"""
		:param lowrange: 双字节码的低字节判定范围: 长度为2的元组
		:param ctrltable: 控制码表: 字典{code: fn(bytes, i) -> (word, i)}
		"""
		self._ct = ct = {}
		self._tc = tc = {}
		self.lowrange = lowrange

		if hasattr(ctrltable, '__len__') and isinstance(ctrltable[0], CtrlCode):
			ctrltable = {ctrlcode.code: ctrlcode for ctrlcode in ctrltable}

		self.ctrltable = ctrltable

		with open(file, 'r', encoding="utf8") as f:
			for line in f.readlines():
				k, v = line.rstrip('\n').split('=', 1)
				k = int(k, 16)
				ct[k] = v
				if len(v) == 1:
					tc[ord(v)] = k

	def decode(self, b):
		if checkbytes(b):
			char = 0
			text = [] # 一句话
			result = []
			i = offset = -1
			length = len(b) - 1

			while i < length:
				i += 1
				byte = b[i]

				if char == 0:
					if self.lowrange and self.lowrange[0] <= byte <= self.lowrange[1]:
						char = byte
						if not text:
							offset = i
						continue
					elif byte == 0x00:
						if text:
							result.append((offset, ''.join(text)))
							text.clear()
						else:
							continue
					else:
						if not text:
							offset = i
						word = self._ct.get(byte, None)
						if word:
							pass
						elif self.ctrltable and byte in self.ctrltable:
							# 控制码表
							word, i = self.ctrltable[byte].decode(b, i)
						else:
							word = '[?%X]' % byte
						text.append(word)
				else:
					char = char << 8 | byte # 低字节在左边
					text.append(self._ct[char])
					char = 0
			if text:
				result.append((offset, ''.join(text)))
			return result
		else:
			print("b must be integer iterable")

	def encode(self, text, buf=None):
		result = bytearray() if buf is None else buf
		length = len(text) - 1
		i = -1

		while i < length:
			i += 1
			ch = text[i]
			code = self._tc.get(ord(ch), 0x00)
			if code == 0:
				if self.ctrltable and CtrlCode.FMT_START.startswith(ch):
					con = False
					for ctrlcode in self.ctrltable.values():
						m = ctrlcode.encode(text, i)
						if m:
							bs, i = m
							i -= 1
							result.extend(bs)
							con = True
							break
					if con:
						continue
				print("warm: %s不在码表中" % ch)
				
			if code > 0xFF:
				result.append(code >> 8)
				result.append(code & 0xFF)
			else:
				result.append(code)
		return result


def fmt2reg(fmt):
	return re.compile(re.escape(fmt).replace('\\%d', '(\w+)'))

class CtrlCode:
	# usage:
	# cc = CtrlCode(0xFC, 'no.%d name[%d]')
	# print(cc.encode('多亏了{no.1 name[1]}的帮助', 3))

	FMT_START = '{'
	FMT_END   = '}'
	FMT_START_LEN = len(FMT_START)
	FMT_END_LEN   = len(FMT_END)

	__slots__ = ('code', 'fmt', 'argc', 'reg')

	def __init__(self, code, fmt):
		self.code = code
		self.fmt = self.FMT_START + fmt + self.FMT_END
		self.argc = fmt.count('%d')
		self.reg = fmt2reg(fmt)

	def decode(self, bs, i):
		if self.argc is 0:
			return self.fmt, i
		if self.argc is 1:
			i += 1
			return self.fmt % bs[i], i
		else:
			return self.fmt % tuple(bs[i] for i in range(self.argc)), i + self.argc

	def encode(self, s, i):
		if self.argc is 0:
			fmt_len = len(self.fmt)
			if s.find(self.fmt, i, i + fmt_len) == i:
				return (self.code,), i + fmt_len
		elif s.find(self.FMT_START, i, i + self.FMT_START_LEN) == i:
			i += self.FMT_START_LEN
			end = s.find(self.FMT_END, i, i + 32)
			if end != -1:
				m = self.reg.match(s[i:end])
				if m:
					return bytes((self.code,) + tuple(int(i) for i in m.groups())), end + self.FMT_END_LEN