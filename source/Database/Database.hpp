#pragma once

#include "../../libs/SQLite3/sqlite3.h"

#include "../Logger.hpp"

#include <vector>
#include <string>

namespace Garmadon {
	bool connected = false;
	sqlite3* DB;

	std::vector<std::pair<char*, const char*>> CurrentData;

	namespace Database {

		int callback(void* data, int argc, char** argv, char** azColName)
		{
			int i;

			for (i = 0; i < argc; i++) {
				CurrentData.emplace_back(azColName[i], argv[i] ? argv[i] : nullptr);
			}

			return 0;
		}

		std::string SearchForVar(const std::vector<std::pair<char*, const char*>>& vectorStore, const char* searchTerm) {
			for (auto item : vectorStore) {
				if (item.first == searchTerm) {
					return std::string(item.second);
				}
			}
			return "";
		}


		void Connect() {
			if (!connected) {
				connected = true;
				sqlite3_open("Caffeine.sqlite", &DB);
			}
		}

		void Disconnect() {
			if (connected) {
				connected = false;
				sqlite3_close(DB);
			}
		}

		void CreateTables() {
			if (connected) {
				std::string sql = "CREATE TABLE IF NOT EXISTS Accounts(ID INT PRIMARY KEY NOT NULL, Username TEXT NOT NULL, Password TEXT  NOT NULL, GMLevel INT NOT NULL); CREATE TABLE IF NOT EXISTS Characters ( CharID integer constraint Characters_pk primary key autoincrement unique, AccountID integer, ObjectID integer, Name text, UnapprovedName text, ShirtColor integer, ShirtStyle integer, PantsColor integer, HairStyle integer, HairColor integer, LeftHand integer, RightHand integer, Eyebrows integer, Eyes integer, Mouth integer, LastZone integer default 1100, Health int default 4, MaxHealth float default 4, Armor int default 0, MaxArmor float default 0, Imagination int default 0, MaxImagination float default 0, InventorySpace int default 20, UScore int default 0, GMLevel int default 0, Reputation int default 0, Level int default 1, X float, Y float, Z float );";
				int result;
				char* error;
				result = sqlite3_exec(DB, sql.c_str(), nullptr, nullptr, &error);

				if (result != SQLITE_OK) {
					Logger::log("Database", "Unable to create tables because (" + std::string(error) + ")");
					sqlite3_free(error);
				}
				else {
					Logger::log("Database", "Verified tables exist.");
				}
			}
			else {
				throw std::exception("Not connected to data base");
			}
		}

		bool CheckLogin(std::string PreUsername, std::string PrePassword) {
			std::string username = std::move(PreUsername);
			std::string sql = "SELECT * FROM Accounts WHERE Username='" + username + "';";

			int result;
			char* error;
			result = sqlite3_exec(DB, sql.c_str(), callback, nullptr, &error);

			if (result != SQLITE_OK) {
				Logger::log("Database", " (" + std::string(error) + ")");
				sqlite3_free(error);
			}
			else {
				std::string SQLresult = SearchForVar(CurrentData, "password");
				if (std::move(PrePassword) == SQLresult) { return true; }
				else { return false; }
			}
			return false;
		}

	}
}