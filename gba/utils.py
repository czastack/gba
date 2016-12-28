def bytesbeautify(b, offset=0, step=1):
	if offset == 0 and step == 1:
		return " ".join("%02X" % x for x in b)

	length = len(b)
	i = offset
	result = []
	fmt = "%%0%dX" % (step << 1)
	while i < length:
		data = j = 0
		while j < step:
			data |= b[i] << (j << 3)
			j += 1
			i += 1
		result.append(fmt % data)
	return " ".join(result)

def strhex(n, size=0):
	"""
	:param size: 字节数
	"""
	if size is 0:
		for x in (0x8, 0x10, 0x20, 0x40, 0x80):
			if n < (1 << x):
				break
		size = x >> 3
	return "%0*X" % ((size << 1), n)

def checkbytes(b):
	return hasattr(b, '__iter__') and type(b[0]) is int