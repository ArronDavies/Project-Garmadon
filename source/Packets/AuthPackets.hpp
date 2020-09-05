#pragma once

#include "../../libs/RakNet/BitStream.h"
#include "../../libs/RakNet/RakPeerInterface.h"

#include "../Utils/Packets.hpp"

namespace Garmadon {
	namespace AuthPackets {
		void HandshakeWithClient(int GameVersion, RakPeerInterface* RakServer, SystemAddress client) {
			RakNet::BitStream bs = RakNet::BitStream();
			Packets::WriteConstruct(&bs, 0x00, 0x00);

			bs.Write<uint32_t>(171022);
			bs.Write<uint32_t>(0x93);
			bs.Write<uint32_t>(1);
			bs.Write<uint32_t>(0);
			bs.Write<uint16_t>(0xff);

			RakServer->Send(&bs, SYSTEM_PRIORITY, RELIABLE_ORDERED, 0, client, false);
		}
	}
}