from .utils import align4

class TextWriter:
	"""
	_writer 要求实现 write(addr, bytes); write32(addr, u32)
	ptrtable 要写入的指针表地址（-1表示不写入文本地址）
	ptrfn 文本地址映射函数 textaddr=ptrfn(addr)
	"""
	__slots__ = ('_dict', '_writer', 'ptrtable', 'ptrfn')

	def __init__(self, di, writer, ptrtable=-1, ptrfn=None):
		self._dict = di
		self._writer = writer
		self.ptrtable = ptrtable
		self.ptrfn = ptrfn

	def write(self, addr, texts):
		for i in range(len(texts)):
			data = self._dict.encode(texts[i])
			self._writer.write(addr, data)

			if ptrtable:
				self._writer.write32(ptrtable + (i << 2), ptrfn(addr))

			addr = align4(addr + len(data))
