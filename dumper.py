from .utils import bytesbeautify
import textwrap

class Dumper:
	__slots__ = ('input', 'output', 'addrmask')

	def __init__(self, input, output=None, addrmask=-1):
		self.input = open(input, 'rb')
		self.output = output
		self.addrmask = addrmask

	def close(self):
		self.input.close()

	__del__ = close

	def read(self, start, size=1):
		return self.pos(start).input.read(size)

	def readUint(self, size=1):
		i = 0
		for x in range(size):
			i |= self.input.read(1)[0] << (x << 3)
		return i

	def read8(self):
		return self.readUint(1)

	def read16(self):
		return self.readUint(2)

	def read32(self):
		return self.readUint(4)

	def pos(self, offset):
		if self.addrmask != -1:
			offset &= self.addrmask
		self.input.seek(offset)
		return self

	def dump(self, start, size):
		if self.output:
			with open(self.output, 'wb') as output:
				return output.write(self.read(start, size))
		else:
			print('unspecified output')

	def print(self, start, size, step=1, word=1, showaddr=False, retstr=False):
		"""
		:param step: 步长字节数
		:param word: 多少个16字节就换行
		:param retstr: True为输出字符串返回，False为直接打印到标准输出 
		"""
		data = bytesbeautify(self.read(start, size), 0, step)
		bytes_per_line = (word << 4)
		width = (bytes_per_line << 1) + bytes_per_line // step
		lines = textwrap.wrap(data, width)
		if retstr:
			result = []
			printfn = result.append
		else:
			printfn = print
		if showaddr:
			addr = start
			for line in lines:
				printfn("%08X %s" % (addr, line))
				addr += bytes_per_line
		else:
			printfn("\n".join(lines))

		if retstr:
			return "\n".join(result)