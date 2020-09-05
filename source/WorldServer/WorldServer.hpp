#pragma once

#include "../../libs/RakNet/RakPeerInterface.h"
#include "../../libs/RakNet/RakNetworkFactory.h"
#include "../../libs/RakNet/RakSleep.h"
#include "../../libs/RakNet/MessageIdentifiers.h"
#include "../../libs/RakNet/BitStream.h"

#include "../Utils/Packets.hpp"
#include "../Logger.hpp"

#define byte uint8_t

namespace Garmadon {
	class World {
	private:
		uint32_t MaxConnections


	public:
		int port;

		int WorldID;

		bool IsCharacterServer = false;

		void SetMaxConnections(uint16_t _MaxConnections) {
			MaxConnections = _MaxConnections;
		}

		World(int _port, int _WorldID) : port(_port), WorldID(_WorldID) {
			if (WorldID == 0) {
				IsCharacterServer = true;
			}

			RakPeerInterface* RakServer = RakNetworkFactory::GetRakPeerInterface();

			RakServer->SetIncomingPassword("3.25 ND1", 8);

			SocketDescriptor socket(1001, nullptr); // Empty IP string = INADDR_ANY

			Logger::log("World", "Starting up World Server");

			bool WorldStarted = RakServer->Startup(MaxConnections, 16, &socket, 1); // Thread sleep time is 16 (That is what live used)

			RakServer->SetMaximumIncomingConnections(MaxConnections);

			if (!WorldStarted) {
				Logger::log("Auth", "Startup failed");

				exit(1);
			}

			Packet* currentPacket;

			while (true) {
				RakSleep(16);
				while (currentPacket = RakServer->Receive()) {
					RakNet::BitStream bs(currentPacket->data, currentPacket->length, false);

					Packets::PacketHeader header = *reinterpret_cast<Packets::PacketHeader*>(currentPacket->data);

					switch (header.RemotePacketID) {
					case ID_USER_PACKET_ENUM: {
						printf("[World] Recieved Packet %02x-%02x-00-%02x \n", header.RemotePacketID, header.RemoteConnectionType, header.PacketID);
						switch (header.RemoteConnectionType) {
						case 00: {
							uint32_t game_version; bs.Read<uint32_t>(game_version);
							uint32_t unknown; bs.Read<uint32_t>(unknown);
							uint32_t remote_connection_type; bs.Read<uint32_t>(remote_connection_type);
							uint32_t process_id; bs.Read<uint32_t>(process_id);
							uint16_t local_port; bs.Read<uint16_t>(local_port);
						} break;
						case 01: {
							// Login response
						} break;
						}
					} break;
					case ID_NEW_INCOMING_CONNECTION: {
						Logger::log("World", "User connected to auth");
					} break;
					case ID_DISCONNECTION_NOTIFICATION: {
						Logger::log("World", "User disconnected from auth");
					} break;
					}
				}

				RakServer->DeallocatePacket(currentPacket);
			}

			RakServer->Shutdown(0);
			RakNetworkFactory::DestroyRakPeerInterface(RakServer);
		}
	};
}
