# Project Garmadon
A Lego Universe server written in Pyhton using lcdr's PyRakNet
This project is not intended for main stream use it is more of a test server that is intended to be reliable.

This version of the server is the last until the rewrite is at the same point.

## Disclaimer
> The LEGO Group has not endorsed or authorized the operation of this game and is not liable for any safety issues in relation to its operation.

## About
This project is very much still in development and there is no working parts from a game play perspective and no one working on this project and or anyone in the LU community are required to give anyone support as this is a piece of server software not meant for widespread use. 

## Contributing 
Any issues that are reported are greatly appreciated and if you think you can do something better than us feel free to open a pull request.

## Prerequisites

You will need Python 3.6 or greater you can find that [here](https://www.python.org/downloads/)

You can find a list of available clients [here](https://docs.google.com/document/d/1XmHXWuUQqzUIOcv6SVVjaNBm4bFg9lnW4Pk1pllimEg), it is recommended you download lcdr's unpacked client. But if you already have a client and don't want to download a new one it is likely that it is packed so you need to unpack it using lcdr's utlis [here](https://bitbucket.org/lcdr/utils).

These prerequisites are needed so that the server can run and are installed when running start.py

[bcrypt](https://pypi.org/project/bcrypt/), [requests](https://pypi.org/project/requests/), [event_dispatcher](https://github.com/lcdr/py_event_dispatcher), [bitstream](https://github.com/lcdr/bitstream), [pyraknet](https://github.com/lcdr/pyraknet), [better_profanity](https://pypi.org/project/better-profanity/).

## Config
Currrently configuration is a quite easy all you need to do is run Start.py and it will generate the SQL table and the config file then copy the maps folder in a unpacked client to the clientfiles folder in the project

## Extra
This server is not meant to be hosted publicly as it is missing many features that LEGO requires a public server to have you can find a list of requirements [here](https://mega.nz/file/Jt1S1SYB#8wC8Ubqq8yQ4-4tVR1y7VrZEkCAUZuaNKjjeZQ6dhe8)

## Credits 
LCDR for his [PyRakNet](https://github.com/lcdr/pyraknet), and any contributer to the LU [documentation](https://docs.google.com/document/d/1v9GB1gNwO0C81Rhd4imbaLN7z-R0zpK5sYJMbxPP3Kc/edit#heading=h.q55eiu5cro7b). 

The TODO list and current known issues can now be found in issues with the tag enhancement.
