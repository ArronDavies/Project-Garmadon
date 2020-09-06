#pragma once

#include "../../libs/RakNet/RakPeerInterface.h"
#include "../../libs/RakNet/RakNetworkFactory.h"
#include "../../libs/RakNet/RakSleep.h"
#include "../../libs/RakNet/MessageIdentifiers.h"
#include "../../libs/RakNet/BitStream.h"

#include "../Utils/Packets.hpp"
#include "../Utils/Strings.hpp"
#include "../Logger.hpp"
#include "../Packets/AuthPackets.hpp"
#include "../Database/Database.hpp"

namespace Garmadon {
	class Auth {
	private:
		uint16_t MaxConnections = 1128;

	public:
		void SetMaxConnections(uint16_t _MaxConnections) {
			MaxConnections = _MaxConnections;
		}

		Auth() {
			RakPeerInterface* RakServer = RakNetworkFactory::GetRakPeerInterface();

			RakServer->SetIncomingPassword("3.25 ND1", 8);

			SocketDescriptor socket(1001, nullptr); // Empty IP string = INADDR_ANY

			Logger::log("Auth", "Starting up Auth Server");

			bool AuthStarted = RakServer->Startup(MaxConnections, 16, &socket, 1); // Thread sleep time is 16 (That is what live used)

			RakServer->SetMaximumIncomingConnections(MaxConnections);
			
			if (!AuthStarted) {
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
						printf("[Auth] Recieved Packet %02x-%02x-00-%02x \n", header.RemotePacketID, header.RemoteConnectionType, header.PacketID);
						switch (header.RemoteConnectionType) {
						case 00: {
							uint32_t game_version; bs.Read<uint32_t>(game_version);
							uint32_t unknown; bs.Read<uint32_t>(unknown);
							uint32_t remote_connection_type; bs.Read<uint32_t>(remote_connection_type);
							uint32_t process_id; bs.Read<uint32_t>(process_id);
							uint16_t local_port; bs.Read<uint16_t>(local_port);

							AuthPackets::HandshakeWithClient(game_version, RakServer, currentPacket->systemAddress);
						} break;
						case 01: {
							std::u16string username = Strings::WStringFromBitStream(&bs);
							std::u16string password = Strings::WStringFromBitStream(&bs, 41);

							if (Database::CheckLogin(username, password)) {
								AuthPackets::LoginResponse(LoginEnum::SUCCESS, RakServer, currentPacket->systemAddress);
							}
						} break;
						}
					} break;
					case ID_NEW_INCOMING_CONNECTION: {
						Logger::log("Auth", "User connected to auth");
					} break;
					case ID_DISCONNECTION_NOTIFICATION: {
						Logger::log("Auth", "User disconnected from auth");
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
