#pragma once

#include "../../libs/RakNet/BitStream.h"
#include "../../libs/RakNet/RakPeerInterface.h"

#include "../Utils/Packets.hpp"
#include "../Enums/LoginEnum.hpp"

namespace Garmadon {
	namespace AuthPackets {
		void HandshakeWithClient(int GameVersion, RakPeerInterface* RakServer, SystemAddress client) {
			RakNet::BitStream bs = RakNet::BitStream();
			Packets::WriteConstruct(&bs, 0x00, 0x00);

			bs.Write<uint32_t>(171022);
			bs.Write<uint32_t>(0x93);
			bs.Write<uint32_t>(1);
			bs.Write<uint32_t>(0);
			bs.Write<uint16_t>(1001);

			RakServer->Send(&bs, SYSTEM_PRIORITY, RELIABLE_ORDERED, 0, client, false);
		}

		void LoginResponse(LoginEnum responseCode, RakPeerInterface* RakServer, SystemAddress client) {
			RakNet::BitStream bs = RakNet::BitStream();
			Packets::WriteConstruct(&bs, 0x05, 0x00); // Construct

			bs.Write<uint8_t>(*reinterpret_cast<uint8_t*>(&responseCode)); // Response code
			bs.Write(std::string(size_t(33 * 8), 0x00)); // Blank strings

			bs.Write<short>(1); // Major version
			bs.Write<short>(10); // Current version
			bs.Write<short>(64); // Minor version

			bs.Write(std::string(size_t(66), 0x63)); // our nice and secure session key :)

			Strings::StringToBitStream(&bs, "127.0.0.1"); // Next Server IP
			Strings::StringToBitStream(&bs, "0.0.0.0"); // Unused Chat IP

			bs.Write<short>(2001); // Next Server port
			bs.Write<short>(0); // Unused Chat port

			Strings::StringToBitStream(&bs, "");

			Strings::StringToBitStream(&bs, "00000000-0000-0000-0000-000000000000", 37);

			bs.Write<long>(0);

			Strings::StringToBitStream(&bs, "US", 3);

			bs.Write<bool>(0); // First time on subscription
			bs.Write<bool>(0); // Free to play?

			bs.Write<long long>(0);

			bs.Write<uint16_t>(0);

			bs.Write<uint32_t>(4);
		}
	}
}