#pragma once

#include "../../libs/RakNet/BitStream.h"

namespace Garmadon {
	namespace PacketUtils {
		class PacketHeader {
		public:
			uint8_t RemotePacketID;
			uint16_t RemoteConnectionType;
			uint32_t PacketID;
			uint8_t paddedbyte;

			PacketHeader(RakNet::BitStream* bs) {
				bs->Read(RemotePacketID);
				bs->Read(RemoteConnectionType);
				bs->Read(PacketID);
				bs->Read(paddedbyte);
			}
		};

	}
}