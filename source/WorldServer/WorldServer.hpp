#pragma once

#include "../../libs/RakNet/RakPeerInterface.h"
#include "../../libs/RakNet/RakNetworkFactory.h"
#include "../../libs/RakNet/RakSleep.h"
#include "../../libs/RakNet/MessageIdentifiers.h"
#include "../../libs/RakNet/BitStream.h"

#include "../Utils/PacketUtils.hpp"
#include "../Logger.hpp"

#define byte uint8_t

namespace Garmadon {
	class World {
	private:
		RakPeerInterface* RakServer;


	public:
		int port;

		int WorldID;

		bool IsCharacterServer = false;

		World(int _port, int _WorldID) : port(_port), WorldID(_WorldID) {
			if (WorldID == 0) {
				IsCharacterServer = true;
			}

			RakServer = RakNetworkFactory::GetRakPeerInterface();

			RakServer->SetIncomingPassword("3.25 ND1", 8);

			SocketDescriptor socket(port, 0);

			Logger::log("Auth", "Starting up Auth Server");

			// TODO: Set max connections to world specific number
			bool AuthStarted = RakServer->Startup(32, 16, &socket, 1); // Thread sleep time is 16 (That is what live used)

			if (!AuthStarted) {
				Logger::log("World", "Startup failed");

				exit(1);
			}

			Packet* currentPacket;

			while (true) {
				while (currentPacket = RakServer->Receive()) {
					RakNet::BitStream bs(currentPacket->data, currentPacket->length, false);

					PacketUtils::PacketHeader header(&bs);

					switch (header.RemotePacketID) {
					case ID_USER_PACKET_ENUM: {
						printf("[World] Recieved Packet %02x-%02x-00-%02x \n", header.RemotePacketID, header.RemoteConnectionType, header.PacketID);
						switch (header.RemoteConnectionType) {
						
						}
					} break;
					case ID_NEW_INCOMING_CONNECTION: {
						Logger::log("World", "Recieving new Connection");
					} break;
					case ID_DISCONNECTION_NOTIFICATION: {
						Logger::log("World", "User Disconnected from World");
					} break;
					}
				}

				RakSleep(1);
			}

			RakServer->Shutdown(-1);
			RakNetworkFactory::DestroyRakPeerInterface(RakServer);

		}
	};
}
