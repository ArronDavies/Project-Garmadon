#pragma once

#include <cstdio>

#if defined(_WIN32) || defined(_WIN64)
#include <Windows.h>
#endif

namespace Garmadon {
	namespace Logger {
#if defined(_WIN32) || defined(_WIN64)
		enum class Color { White = 23, Red = 4, Blue = 1, Green = 2, Cyan = 3, Purple = 5 };
#else
		enum class Color { White = 37, Red = 31, Blue = 34, Green = 32, Cyan = 36, Purple = 35 };
#endif

		void log(const std::string& server, const std::string& message, Color LogType = Color::White) {
#if defined(_WIN32) || defined(_WIN64)
			HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
			int k;

			if (LogType != Color::White) {
				SetConsoleTextAttribute(hConsole, (int)LogType);
			}
			std::cout << "[" << server.c_str() << "] " << message.c_str() << " \n";
#else
			std::cout << "\033[1;" << std::to_string((int)LogType) << "m[" << server.c_str() << "] " << message.c_str() << " \n";
#endif
		}
	}
}