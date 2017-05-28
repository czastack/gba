import struct

def goto(to, r=0, align4=True):
	"""
	利用r15实现任意地址跳转
	:param r: 0~7
	:param to: 目标地址
	:param align4: 要写入代码的地址是否对齐4
	"""
	code = bytearray(b'\x00\x48\x87\x46')
	if 0 < r < 8:
		code[1] += r
		code[2] += r << 3

	if not align4:
		code[0] += 1
		code += b'\x00\x00'

	code += struct.pack('1L', to)
	return bytes(code)
	