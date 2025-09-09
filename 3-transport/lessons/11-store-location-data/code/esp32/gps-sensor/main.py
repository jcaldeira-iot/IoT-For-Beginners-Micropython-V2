import network

ssid = '<NETWORK_SSID>'
password = '<NETWORK_PASSWORD>'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
print('network config:', wlan.ipconfig('addr4'))

try:
    import ioth
except:
    import mip
    mip.install('github:jcaldeira-iot/iot-hub-micropython-client/package.json')
    import ioth
from ioth import IoTHClient

iot_hub = '<hub_name>.azure-devices.net'
device_id = 'soil-moisture-sensor'
sas_token = '<sas_token>'

device_client = IoTHClient(iot_hub, device_id, sas_token)

print('Connecting')
device_client.connect()
print('Connected')

import time
import json

gpsDataFile = open('gpsTrack.gpx', 'r')

def print_gps_data(data):
    data = data.strip()
    if 'trkpt lat=' in data:
        parts = data.split('"')
        lat = float(parts[1])
        lon = float(parts[3])
        
        telemetry = json.dumps({ "gps" : { "lat":lat, "lon":lon } })
        print("Sending telemetry ", telemetry)
        device_client.send_telemetry(telemetry)

while True:
    data = gpsDataFile.readline()
    if data:
        print_gps_data(data)
    else:
        print("End of file start again!!!")
        gpsDataFile.close()
        gpsDataFile = open('gpsTrack.gpx', 'r')
    time.sleep(1)