import json
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
from ioth import IoTHClient, IoTHEvents

iot_hub = '<hub_name>.azure-devices.net'
device_id = 'soil-moisture-sensor'
sas_token = '<sas_token>'

device_client = IoTHClient(iot_hub, device_id, sas_token)

print('Connecting')
device_client.connect()
print('Connected')

import time
from machine import ADC, Pin

adc = ADC(7, atten=ADC.ATTN_11DB)
relay = Pin(15, Pin.OUT)

def handle_method_request(request, ack):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()
    
    ack(request, "200")

device_client.on(IoTHEvents.COMMANDS, handle_method_request)

sec_count = 0
while True:
    if sec_count == 0:
        soil_moisture = adc.read()
        telemetry = json.dumps({'soil_moisture' : soil_moisture})
        print("Sending telemetry ", telemetry)
        device_client.send_telemetry(telemetry)
    
    device_client.listen()
    
    sec_count = (sec_count + 1) % 10
    time.sleep(1)
