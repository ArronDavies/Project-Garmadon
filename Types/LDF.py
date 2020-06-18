import bitstream
from xml.etree import ElementTree
from Enums import LEGO_DATA_TYPES


class LDF(bitstream.Serializable):
    """
    Lego Data Format
    """

    def __init__(self):
        self._keys: list = []

    def register_key(self, key_name: str, value: any, value_type: int):
        self._keys.append([key_name, value, value_type])

    def serialize(self, stream: bitstream.WriteStream) -> None:
        key_num = len(self._keys)
        stream.write(bitstream.c_uint(key_num))
        for key in self._keys:
            name = key[0]
            value = key[1]
            value_type = key[2]
            stream.write(bitstream.c_uint8(len(name) * 2))
            for char in name:
                stream.write(char.encode('latin1'))
                stream.write(b'\0')
            stream.write(bitstream.c_ubyte(value_type))
            if value_type == 0:
                stream.write(value, length_type=bitstream.c_uint)
            elif value_type == 1:
                stream.write(bitstream.c_int(value))
            elif value_type == 3:
                stream.write(bitstream.c_float(value))
            elif value_type == 5:
                stream.write(bitstream.c_uint(value))
            elif value_type == 7:
                stream.write(bitstream.c_bool(value))
            elif value_type == 8 or value_type == 9:
                stream.write(bitstream.c_int64(value))
            elif value_type == 13:
                xml_str = bytes(ElementTree.tostring(value))
                xml_str = b'<?xml version="1.0">' + xml_str
                stream.write(bitstream.c_ulong(xml_str.__len__()))
                stream.write(xml_str)

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This struct cannot be deserialized")
