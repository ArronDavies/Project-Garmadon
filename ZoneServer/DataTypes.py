from bitstream import *
from xml.etree import ElementTree


class Vector4(Serializable):
    """
    Vector4
    """

    def __init__(self, x, y, z, w=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    @classmethod
    def deserialize(cls, stream):
        x = stream.read(c_float)
        y = stream.read(c_float)
        z = stream.read(c_float)
        w = stream.read(c_float)

        return cls(x, y, z, w)

    @classmethod
    def from_array(cls, arr):
        """
        Creates a Vector4 from an array
        """
        return cls(arr[0], arr[1], arr[2], arr[3])

    @classmethod
    def from_vec3(cls, vec):
        """
        Creates a Vector4 from a Vector3
        """
        return cls(vec.x, vec.y, vec.z, 0)

    def serialize(self, stream):
        stream.write(c_float(self.x))
        stream.write(c_float(self.y))
        stream.write(c_float(self.z))
        stream.write(c_float(self.w))


class Vector3(Serializable):
    """
    Vector3
    """

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def deserialize(cls, stream):
        x = stream.read(c_float)
        y = stream.read(c_float)
        z = stream.read(c_float)

        return cls(x, y, z)

    @classmethod
    def from_array(cls, arr):
        """
        Creates a Vector3 from an array
        """
        return cls(arr[0], arr[1], arr[2])

    @classmethod
    def from_ldf(cls, ldf_val):
        """
        Creates a Vector3 from a ldf value
        """
        arr = ldf_val.split('\x1f')
        return cls(arr[0], arr[1], arr[2])

    def serialize(self, stream):
        stream.write(c_float(self.x))
        stream.write(c_float(self.y))
        stream.write(c_float(self.z))


LEGO_DATA_TYPES = {
    str: 0,
    c_int32: 1,
    c_float: 3,
    c_double: 4,
    c_uint32: 5,
    c_bool: 7,
    c_int64: 8,
}


class LDF(Serializable):
    """
    LDF key serializable
    """
    def __init__(self, key, data, data_type, data_num=None):
        self.key = key
        self.data = data
        self.data_type = data_type
        self.data_num = data_num

    def serialize(self, stream):
        stream.write(c_uint8(len(self.key) * 2))

        for char in self.key:
            stream.write(char.encode('latin1'))
            stream.write(b'\0')

        if not self.data_num:
            if isinstance(self.data, ElementTree.Element):
                stream.write(c_uint8(13))

                txt = b'<?xml version="1.0">' + ElementTree.tostring(self.data)

                stream.write(c_uint32(len(txt)))
                stream.write(txt)
            else:
                stream.write(c_uint8(LEGO_DATA_TYPES[self.data_type]))

                if self.data_type == str:
                    stream.write(self.data, length_type=c_uint)
                else:
                    stream.write(self.data_type(self.data))
        else:
            stream.write(c_uint8(self.data_num))
            stream.write(self.data)

    def deserialize(self, stream):
        return "Not Implemented"


class LegoData(Serializable):
    def __init__(self):
        self.keys = []

    def write(self, key, data, data_type=None, data_num=None):
        ldf_key = LDF(key, data, data_type)

        self.keys.append(ldf_key)

    def serialize(self, stream):
        super().serialize(stream)

        stream.write(c_uint32(len(self.keys)))

        for key in self.keys:
            key.serialize(stream)

    @classmethod
    def deserialize(cls, stream):
        return cls()