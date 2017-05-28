import struct

class FileRW:
	__slots__ = ('_file', 'addrmask')

	MODE = 'rb'

	def __init__(self, input, addrmask=~(1<<27), mode=None):
		self._file = open(input, mode or self.MODE)
		self.addrmask = addrmask

	def close(self):
		self._file.close()

	__del__ = close

	def pos(self, offset):
		if self.addrmask != -1:
			offset &= self.addrmask
		self._file.seek(offset)
		return self

	def read(self, start, size=1):
		return self.pos(start)._file.read(size)

	def readUint(self, size):
		i = 0
		for x in range(size):
			i |= self._file.read(1)[0] << (x << 3)
		return i

	def readFmt(self, fmt, size):
		return struct.unpack(fmt, self._file.read(size))

	def read8(self):
		return self.readFmt('B', 1)

	def read16(self):
		return self.readFmt('H', 2)

	def read32(self):
		return self.readFmt('L', 4)

	def write(self, start, data):
		return self.pos(start)._file.write(data)

	def writeFmt(self, fmt, data):
		return self._file.write(struct.pack(fmt, data))

	def write8(self, data):
		return self.writeFmt('B', data)

	def write16(self, data):
		return self.writeFmt('H', data)

	def write32(self, data):
		return self.writeFmt('L', data)

	def patchFile(self, addr, file, offset=0, size=-1):
		with open(file, 'rb') as f:
			if offset:
				f.seek(offset)
			self.write(addr, f.read(size))