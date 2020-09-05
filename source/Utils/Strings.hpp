#pragma once

#include "../../libs/RakNet/BitStream.h"

#include <string>

namespace Garmadon {
	namespace Strings {
		void StringToBitStream(RakNet::BitStream* bs, std::string data, unsigned int length = 33) {
			if (data.length() > len) { text = text.substr(0, length); }
			bs->Write(text.c_str(), static_cast<const unsigned int>(text.length()));
			bs->Write(std::string(length - static_cast<unsigned int>(data.length()), 0x00).c_str(), length - static_cast<unsigned int>(data.length()));
		}
	}
}