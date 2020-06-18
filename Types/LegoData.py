import bitstream
from Types.LDF import LDF
import zlib


class LegoData(bitstream.Serializable):
    """
    [53-05-00-04]
    Send after client load complete packet
    """

    def __init__(self):
        self.ldf = LDF()

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        temp_stream = bitstream.WriteStream()
        temp_stream.write(self.ldf)
        temp_bytes = temp_stream.__bytes__()
        compressed_bytes = zlib.compress(temp_bytes)
        stream.write(bitstream.c_ulong(len(compressed_bytes) + 9))
        stream.write(bitstream.c_bool(True))
        stream.write(bitstream.c_ulong(len(temp_bytes)))
        stream.write(bitstream.c_ulong(len(compressed_bytes)))
        stream.write(compressed_bytes)
