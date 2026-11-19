import time
import network
import json

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

import urequests as requests

service_url = 'https://gps-sensor-iot.<your-subdomain>.workers.dev'
device_id = 'gps-sensor'
device_key = '<device key>'

def send_telemetry(telemetry):
    response = requests.post(
        service_url + '/telemetry',
        data=telemetry,
        headers={
            'Content-Type': 'application/json',
            'x-device-id': device_id,
            'x-api-key': device_key,
        },
    )
    try:
        if response.status_code != 200:
            raise RuntimeError('HTTP {}: {}'.format(response.status_code, response.text))
        return response.json()
    finally:
        response.close()

gpsDataFile = open('gpsTrack.gpx', 'r')

def print_gps_data(data):
    data = data.strip()
    if 'trkpt lat=' in data:
        parts = data.split('"')
        lat = float(parts[1])
        lon = float(parts[3])

        telemetry = json.dumps({ "gps" : {"lat" : lat, "lon" : lon}})
        print("Sending telemetry ", telemetry)
        try:
            reply = send_telemetry(telemetry)
            print("Reply ", reply)
        except Exception as e:
            print("Error:", e)

while True:
    data = gpsDataFile.readline()
    if data:
        print_gps_data(data)
    else:
        print("End of file!")
        gpsDataFile.close()
        break
    time.sleep(1)
