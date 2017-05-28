from .file import FileRW
from .utils import bytesbeautify
import textwrap

class Dumper(FileRW):

	def dump(self, output, start, size):
		with open(output, 'wb') as fo:
			return fo.write(self.read(start, size))

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
