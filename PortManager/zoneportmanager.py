import upnpy
import socket

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
    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=auth_info['Port'],
        NewProtocol='TCP',
        NewInternalPort=auth_info['Port'],
        NewInternalClient=localip,
        NewEnabled=1,
        NewPortMappingDescription='PikaChewniverse Zone Server',
        NewLeaseDuration=0
    )
except upnpy.exceptions.IGDError:
    print("No UPNP available device found")