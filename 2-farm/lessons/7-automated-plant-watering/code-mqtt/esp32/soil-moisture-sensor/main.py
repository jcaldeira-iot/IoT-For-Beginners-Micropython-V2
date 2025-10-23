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

from umqtt.simple import MQTTClient

import time
from machine import ADC, Pin

adc = ADC(7, atten=ADC.ATTN_11DB)
relay = Pin(15, Pin.OUT)

id = '<ID>'
client_name = id + 'soilmoisturesensor_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = MQTTClient(client_name, 'test.mosquitto.org')
mqtt_client.connect()
print("MQTT connected!")

def handle_command(topic, message):
  payload = json.loads(message.decode())
  print("Message received:", payload)

  if payload['relay_on']:
    relay.on()
  else:
    relay.off()

mqtt_client.set_callback(handle_command)
mqtt_client.subscribe(server_command_topic)

while True:
  soil_moisture = adc.read()
  telemetry = json.dumps({'soil_moisture' : soil_moisture})
  
  print("Sending telemetry ", telemetry)

  mqtt_client.publish(client_telemetry_topic, telemetry)

  mqtt_client.check_msg()
    
  time.sleep(10)
