#pragma once

#include "../../libs/RakNet/BitStream.h"

#include <string>
#include <memory>

namespace Garmadon {
	namespace Strings {
		void StringToBitStream(RakNet::BitStream* bs, std::string data, unsigned int length = 33) {
			if (data.length() > length) { data = data.substr(0, length); }
			bs->Write(data.c_str(), static_cast<const unsigned int>(data.length()));
			bs->Write(std::string(length - static_cast<unsigned int>(data.length()), 0x00).c_str(), length - static_cast<unsigned int>(data.length()));
		}

		std::u16string WStringFromBitStream(RakNet::BitStream* bs, unsigned int length = 33) {
			std::unique_ptr<char[]> buffer = std::make_unique<char[]>(length * 2);
			bs->Read(buffer.get(), length * 2);

			char16_t* data = reinterpret_cast<char16_t*>(buffer.get());

			int i;
			for (i = 0; 1 < length; ++i) {
				if (*(data + i) == 0x0000) break;
			}

			return std::u16string(reinterpret_cast<char16_t*>(buffer.get(), i));
		}
	}
}