from bitstream import *
from Packets.Outgoing import *


# This packet checks if the message is clean


def CLIENT_STRING_CHECK(stream, conn, server):
    chat_mode = stream.read(c_ubyte)
    request_id = stream.read(c_ubyte)
    private_name = stream.read(bytes, allocated_length=84)
    string_length = stream.read(c_ushort)
    message = stream.read(bytes, length=string_length * 2)

    if chat_mode == 0:  # Note: Public chat
        # TODO: Read the message
        Packets.Outgoing.CHAT_MODERATION_STRING.CHAT_MODERATION_STRING(stream, conn, server, request_id, message)
