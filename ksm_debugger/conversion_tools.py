import struct

def read_bytes(byte_iter, num):
    """Reads num bytes from a ByteIterator"""
    byte_list = []

    for i in range(num):
        byte_list.append(next(byte_iter))
    
    byte_list = b''.join(byte_list)
    
    return bytearray(byte_list)

def btoi_l(bytev: bytes, signed=True) -> int:
    """Converts a bytes object to an int in LITTLE-endian format"""
    return int.from_bytes(bytev, byteorder='little', signed=signed)

def btoi_b(byte: bytes, signed=True) -> int:
    """Converts a bytes object to an int in BIG-endian format"""
    return int.from_bytes(byte, byteorder='big', signed=signed)

def btob(byte: bytes) -> bool:
    """Converts a bytes object to a bool"""
    return bool(btoi_l(byte))

def btoh_l(byte: bytes) -> int:
    """Converts a bytes object to a short word in LITTLE-endian format"""
    return btoi_l(byte)

def btoh_b(byte: bytes) -> int:
    """Converts a bytes object to a short word in BIG-endian format"""
    return btoi_b(byte)

def btow_l(byte: bytes) -> int:
    """Converts a bytes object to a word in LITTLE-endian format"""
    return btoi_l(byte)

def btow_b(byte: bytes) -> int:
    """Converts a bytes object to a word in BIG-endian format"""
    return btoi_b(byte)

def btof_l(byte: bytes) -> int:
    """Converts a bytes object to a float in LITTLE-endian format"""
    return struct.unpack('<f', byte)[0]

def btof_b(byte: bytes) -> int:
    """Converts a bytes object to a float in BIG-endian format"""
    return struct.unpack('>f', byte)[0]

def btod_l(byte: bytes) -> int:
    """Converts a bytes object to a double in LITTLE-endian format"""
    return struct.unpack('<d', byte)[0]

def btod_b(byte: bytes) -> int:
    """Converts a bytes object to a double in BIG-endian format"""
    return struct.unpack('>d', byte)[0]

def btol_l(byte: bytes) -> int:
    """Converts a bytes object to a long in LITTLE-endian format"""
    return struct.unpack('<l', byte)[0]

def btol_b(byte: bytes) -> int:
    """Converts a bytes object to a long in BIG-endian format"""
    return struct.unpack('>l', byte)[0]

def btos(byte: bytes) -> str:
    """Converts a bytes object to a string"""
    return byte.decode('UTF-8')