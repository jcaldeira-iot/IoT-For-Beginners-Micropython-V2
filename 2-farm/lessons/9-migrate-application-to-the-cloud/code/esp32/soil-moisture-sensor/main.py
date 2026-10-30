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

import urequests as requests

import time
from machine import ADC, Pin

adc = ADC(7, atten=ADC.ATTN_11DB)
relay = Pin(15, Pin.OUT)

service_url = 'https://soil-moisture-iot.<your-subdomain>.workers.dev'
device_id = 'soil-moisture-sensor'
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

def handle_command(command):
    print("Command received - ", command)

    if command == "relay_on":
        relay.on()
        time.sleep(20)
        relay.off()
    elif command == "relay_off":
        relay.off()

def handle_reply(reply):
    command = reply.get('command')
    if command is not None:
        handle_command(command)

while True:
    soil_moisture = adc.read()
    telemetry = json.dumps({'soil_moisture' : soil_moisture})
    print("Sending telemetry ", telemetry)

    try:
        reply = send_telemetry(telemetry)
        handle_reply(reply)
    except Exception as e:
        print("Error:", e)

    time.sleep(10)