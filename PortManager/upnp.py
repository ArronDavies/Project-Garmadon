import upnpy
import configparser
import socket

config = configparser.ConfigParser() # TODO integrate this into each server so it can be split up and still work
config.read('../config.ini')
zone_info = config['ZONE']
auth_info = config['AUTH']
char_info = config['CHARACTER']
master_info = config['MASTER']

try:
    localip = socket.gethostbyname(socket.gethostname())
    if localip == "127.0.0.1":
        localip = socket.gethostbyname_ex(socket.gethostname())[-1]
    else:
        pass
except:
    print("UPNP failed please port forward manually")
    exit()

upnp = upnpy.UPnP()
try:
    device = upnp.get_igd()
    device.get_services()
    service = device['WANPPPConnection.1']
    service.get_actions()
    service.AddPortMapping.get_input_arguments()
    service.AddPortMapping( # TODO This is not how we want to do it because there is the possiblility of 2 auths on 1 ip but it works for now
        NewRemoteHost='',
        NewExternalPort=auth_info['Port'],
        NewProtocol='TCP',
        NewInternalPort=auth_info['Port'],
        NewInternalClient=localip,
        NewEnabled=1,
        NewPortMappingDescription='PikaChewniverse Authentication Server',
        NewLeaseDuration=0
    )
    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=char_info['Port'],
        NewProtocol='TCP',
        NewInternalPort=char_info['Port'],
        NewInternalClient=localip,
        NewEnabled=1,
        NewPortMappingDescription='PikaChewniverse Character Server',
        NewLeaseDuration=0
    )
    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=master_info['Port'],
        NewProtocol='TCP',
        NewInternalPort=master_info['Port'],
        NewInternalClient=localip,
        NewEnabled=1,
        NewPortMappingDescription='PikaChewniverse Master Server',
        NewLeaseDuration=0
    )
    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=zone_info['Port'],
        NewProtocol='TCP',
        NewInternalPort=zone_info['Port'],
        NewInternalClient=localip,
        NewEnabled=1,
        NewPortMappingDescription='PikaChewniverse Zone Server',
        NewLeaseDuration=0
    )
except upnpy.exceptions.IGDError:
    print("No UPNP available device found")