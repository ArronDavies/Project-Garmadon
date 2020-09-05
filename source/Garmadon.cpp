#include <iostream>

#include "AuthServer/AuthServer.hpp"
#include "Database/Database.hpp"

using namespace Garmadon;

int main() {
	Logger::LogToConsole = true;
	Logger::log("Main", "Verifying tables");
	
	Database::Connect();
	Database::CreateTables();

	Logger::log("Main", "Starting Auth server");
	Auth AuthServer = Auth();

	return 0;
}