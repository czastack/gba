from .utils import checkbytes

class Dictionary:
	__slots__ = ('_ct', '_tc', 'lowrange')

	def __init__(self, file, lowrange=None):
		"""
		:param lowrange: 双字节码的低字节判定范围: 长度为2的元组
		"""
		self._ct = ct = {}
		self._tc = tc = {}
		self.lowrange = lowrange
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
			i = offset = 0
			for byte in b:
				i += 1
				if char == 0:
					if self.lowrange and self.lowrange[0] <= byte <= self.lowrange[1]:
						char = byte
						if not text:
							offset = i - 1
						continue
					elif byte == 0x00:
						if text:
							result.append((offset, ''.join(text)))
							text = []
						else:
							continue
					else:
						tmp = self._ct.get(byte, None)
						if tmp:
							if not text:
								offset = i - 1
							text.append(tmp)
				else:
					char = char << 8 | byte # 低字节在左边
					text.append(self._ct[char])
					char = 0
			if text:
				result.append((offset, ''.join(text)))
			return result
		else:
			print("b must be integer iterable")

	def encode(self, s):
		result = bytearray()
		for ch in s:
			code = self._tc.get(ord(ch), 0x00)
			if code == 0:
				print("warm: %s不在码表中" % ch)
			if code > 0xFF:
				result.append(code >> 8)
				result.append(code & 0xFF)
			else:
				result.append(code)
		return result