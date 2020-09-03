cmake_minimum_required (VERSION 3.8)
project ("Project Garmadon")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_definitions(-D_CRT_SECURE_NO_WARNINGS)
add_definitions(-D_WINSOCK_DEPRECATED_NO_WARNINGS)

message("-- Began Garmadon CMake")

if(UNIX AND NOT APPLE)
    set(LINUX TRUE)
endif()

if (NOT EXISTS output)
    file(MAKE_DIRECTORY output)
endif()

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/output)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/output)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/output)

add_subdirectory(libs)

add_executable (Garmadon "source/Garmadon.cpp" "source/AuthServer/AuthServer.hpp" "source/Logger.hpp"  "source/Utils/PacketUtils.hpp" "source/WorldServer/WorldServer.hpp")
set_target_properties(Garmadon PROPERTIES LINKER_LANGUAGE CXX)

target_link_libraries(Garmadon RakNet)
