from bitstream import *
from Packets.Outgoing import *
from Types.LWOOBJID import LWOOBJID
import linecache
from uuid import uuid3, uuid4, NAMESPACE_DNS
from Utils.GetShirtLOT import GetShirtLOT
from Utils.GetPantsLOT import GetPantsLOT


# Sent when creating a character

def CLIENT_CHARACTER_CREATE_REQUEST(stream, conn, server):
    address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
    uid = str(uuid3(NAMESPACE_DNS, str(address)))
    session = server.get_session(uid)

    char_dict = {}

    name = stream.read(str, allocated_length=33)  # wstring 66 bytes
    first_name = stream.read(c_ulong)
    second_name = stream.read(c_ulong)
    third_name = stream.read(c_ulong)
    unknown = stream.read(bytes, allocated_length=9)
    char_dict['ShirtColor'] = stream.read(c_ulong)
    char_dict['ShirtStyle'] = stream.read(c_ulong)
    char_dict['PantsColor'] = stream.read(c_ulong)
    char_dict['HairStyle'] = stream.read(c_ulong)
    char_dict['HairColor'] = stream.read(c_ulong)
    char_dict['LeftHand'] = stream.read(c_ulong)
    char_dict['RightHand'] = stream.read(c_ulong)
    char_dict['Eyebrows'] = stream.read(c_ulong)
    char_dict['Eyes'] = stream.read(c_ulong)
    char_dict['Mouth'] = stream.read(c_ulong)
    unknown2 = stream.read(c_ubyte)

    char_dict['ObjectID'] = LWOOBJID().generate(persistent=True, character=True)

    firstname = linecache.getline('clientfiles/minifigname_first.txt', first_name + 1)  # First Name
    middlename = linecache.getline('clientfiles/minifigname_middle.txt', second_name + 1)  # Second Name
    lastname = linecache.getline('clientfiles/minifigname_last.txt', third_name + 1)  # Third Name
    unapproved_name = firstname.rstrip() + middlename.rstrip() + lastname.rstrip()  # All 3
    char_dict['UnapprovedName'] = unapproved_name
    if name is None:
        char_dict['Name'] = name
        char_dict['UnapprovedName'] = unapproved_name
    else:
        char_dict['UnapprovedName'] = name
        char_dict['Name'] = unapproved_name
    response = session.create_character(character=char_dict)


    char = session.current_character

    pantsLot = GetPantsLOT(char_dict['PantsColor'])
    item_id = LWOOBJID().generate()
    item = {"ItemID": item_id, "IsEquipped": 1, "IsLinked": 1, "Quantity": 1, "ItemLOT": pantsLot, "Type": 0}
    char.add_item(item)

    shirtLot = GetShirtLOT(Color=char_dict['ShirtColor'], Style=char_dict['ShirtStyle'])
    item_id = LWOOBJID().generate()
    item2 = {"ItemID": item_id, "IsEquipped": 1, "IsLinked": 1, "Quantity": 1, "ItemLOT": shirtLot, "Type": 0}
    char.add_item(item2)
    # Used to set character item details

    if response == 0x00:  # Note: Successful
        CHARACTER_CREATE_RESPONSE.CHARACTER_CREATE_RESPONSE(stream, conn, response)
        CHARACTER_LIST_RESPONSE.CHARACTER_LIST_RESPONSE(stream, conn, server)
    else:
        CHARACTER_CREATE_RESPONSE.CHARACTER_CREATE_RESPONSE(stream, conn, response)
