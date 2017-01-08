import ctypes
from dllhelper import DllHelper

class VbaHelper(DllHelper):

	__libname__ = __file__, 'vbacontrol'

	@classmethod
	def fnsign(cls):
		u8  = ctypes.c_uint8
		u16 = ctypes.c_uint16
		u32 = ctypes.c_uint32
		c_bool = ctypes.c_bool
		return (
			('attach', None, c_bool),
			('read8', [u32], u8),
			('read16', [u32], u16),
			('read32', [u32], u32),
			('write8', [u32, u8], c_bool),
			('write16', [u32, u16], c_bool),
			('write32', [u32, u32], c_bool),
			('readBytes', [u32, ctypes.c_size_t, ctypes.c_char_p], c_bool),
			('writeBytes', [u32, ctypes.c_size_t, ctypes.c_char_p], c_bool),
		)

	def attach(self):
		return self.clib.attach()

	def read8(self, addr):
		return self.clib.read8(addr)

	def read16(self, addr):
		return self.clib.read16(addr)

	def read32(self, addr):
		return self.clib.read32(addr)

	def write8(self, addr, data):
		return self.clib.write8(addr, data)

	def write16(self, addr, data):
		return self.clib.write16(addr, data)

	def write32(self, addr, data):
		return self.clib.write32(addr, data)

	def read(self, addr, size):
		buf = ctypes.create_string_buffer(size)
		self.clib.readBytes(addr, size, buf)
		return buf.raw

	def write(self, addr, data):
		"""
		:param data: bytes
		"""
		buf = ctypes.create_string_buffer(data)
		return self.clib.writeBytes(addr, len(data), buf)

	def patchFile(self, addr, file):
		with open(file, 'rb') as f:
			self.write(addr, f.read())
