import ctypes
from dllhelper import DllHelper

class GbaEmuHelper(DllHelper):
	__slots__ = ('this',)

	__libname__ = __file__, 'vbacontrol'

	def __del__(self):
		self.close()

	@classmethod
	def fnsign(cls):
		u8  = ctypes.c_uint8
		u16 = ctypes.c_uint16
		u32 = ctypes.c_uint32
		c_bool = ctypes.c_bool
		this_t = ctypes.c_void_p

		return (
			('VbaHandler_new', None, this_t),
			('NogbaHandler_new', None, this_t),
			('attach', [this_t], c_bool),
			('read8', [this_t, u32], u8),
			('read16', [this_t, u32], u16),
			('read32', [this_t, u32], u32),
			('write8', [this_t, u32, u8], c_bool),
			('write16', [this_t, u32, u16], c_bool),
			('write32', [this_t, u32, u32], c_bool),
			('read', [this_t, u32, ctypes.c_size_t, ctypes.c_char_p], c_bool),
			('write', [this_t, u32, ctypes.c_size_t, ctypes.c_char_p], c_bool),
			('close', [this_t], None),
		)

	def attach(self):
		return self.clib.attach(self.this)

	def close(self):
		if self.this:
			self.clib.close(self.this)
			self.this = None

	def read8(self, addr):
		return self.clib.read8(self.this, addr)

	def read16(self, addr):
		return self.clib.read16(self.this, addr)

	def read32(self, addr):
		return self.clib.read32(self.this, addr)

	def write8(self, addr, data):
		return self.clib.write8(self.this, addr, data)

	def write16(self, addr, data):
		return self.clib.write16(self.this, addr, data)

	def write32(self, addr, data):
		return self.clib.write32(self.this, addr, data)

	def read(self, addr, size):
		buf = ctypes.create_string_buffer(size)
		self.clib.read(self.this, addr, size, buf)
		return buf.raw

	def write(self, addr, data):
		"""
		:param data: bytes
		"""
		buf = ctypes.create_string_buffer(data)
		return self.clib.write(self.this, addr, len(data), buf)

	def patchFile(self, addr, file):
		with open(file, 'rb') as f:
			self.write(self.this, addr, f.read())


class VbaHelper(GbaEmuHelper):
	def __init__(self):
		super().__init__()
		self.this = self.clib.VbaHandler_new()


class NogbaHelper(GbaEmuHelper):
	def __init__(self):
		super().__init__()
		self.this = self.clib.NogbaHandler_new()