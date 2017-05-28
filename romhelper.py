from .file import FileRW

class RomRW(FileRW):

	def write8(self, addr, data):
		self.pos(addr)
		return FileRW.write8(self, data)

	def write16(self, addr, data):
		self.pos(addr)
		return FileRW.write16(self, data)

	def write32(self, addr, data):
		self.pos(addr)
		return FileRW.write32(self, data)