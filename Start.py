import asyncio
import os
import os.path
from os import path
import logging
import configparser
import socket

if path.exists("config.ini"):
    config = configparser.ConfigParser()
    config.read('config.ini')
    char_info = config['CHARACTER']
    master_info = config['MASTER']
    zone_info = config['ZONE']
    auth_info = config['AUTH']

serverType = "[Start]"


def firewall_check():
    master_check()
    auth_check()
    char_check()
    zone_check()


def master_check():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port = master_info['Port']
        s.connect(("127.0.0.1", int(port)))
        s.shutdown(2)
    except:
        print("[Master] Ports Open")


def auth_check():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port = auth_info['Port']
        s.connect(("127.0.0.1", int(port)))
        s.shutdown(2)
    except:
        print("[Auth] Ports Open")


def char_check():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port = char_info['Port']
        s.connect(("127.0.0.1", int(port)))
        s.shutdown(2)
    except:
        print("[Char] Ports Open")


def zone_check():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port = zone_info['Port']
        s.connect(("127.0.0.1", int(port)))
        s.shutdown(2)
    except:
        print("[Zone] Ports Open")


def server_start():  # TODO Multithreading with correct working dir stuff
    pass

def create_config():
    f = open("config.ini", "a+")
    f.write("[MASTER]")
    f.write("\nHost = 127.0.0.1")
    f.write("\nBindip = 0.0.0.0")
    f.write("\nPort = 5000")
    f.write("\n ")
    f.write("\n[AUTH]")
    f.write("\nHost = 127.0.0.1")
    f.write("\nBindip = 0.0.0.0")
    f.write("\nPort = 1001")
    f.write("\nAPIPort = 5001")
    f.write("\n ")
    f.write("\n[CHARACTER]")
    f.write("\nHost = 127.0.0.1")
    f.write("\nBindip = 0.0.0.0")
    f.write("\nPort = 1002")
    f.write("\nAPIPort = 5002")
    f.write("\n ")
    f.write("\n[ZONE]")
    f.write("\nBindip = 127.0.0.1")
    f.write("\n ")
    f.write("\n[CHAT]")
    f.write("\nHost = 127.0.0.1")
    f.write("\nBindip = 127.0.0.1")
    f.write("\nPort = 3000")
    f.write("\n")
    f.write("\n[PORT_HANDLING]")
    f.write("\nUPNP = True")
    f.close()


def main():
    if path.exists("config.ini"):
        print(serverType, "Config exists starting server")
        server_start()
    else:
        print(serverType, "Config file was created please populate it.")
        create_config()
        exit()


if __name__ == "__main__":
    if path.exists("config.ini"):
        firewall_check()
        main()
    else:
        main()
