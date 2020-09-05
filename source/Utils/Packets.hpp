#pragma once

#include "../../libs/RakNet/BitStream.h"

typedef uint8_t byte;

namespace Garmadon {
	namespace Packets {
		struct PacketHeader {
			uint8_t RemotePacketID;
			uint16_t RemoteConnectionType;
			uint32_t PacketID;
			uint8_t paddedbyte;
		}; 

		void WriteConstruct(RakNet::BitStream* bs, uint16_t rct, uint32_t ipid) {
			bs->Write<uint8_t>(0x53);
			bs->Write<uint16_t>(rct);
			bs->Write<uint32_t>(ipid);
			bs->Write<uint8_t>(0x00);
		}
	}
}