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

light_sensor = ADC(5, atten=ADC.ATTN_0DB)
led = Pin(4, Pin.OUT)

id = '<ID>'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = MQTTClient(client_name, 'test.mosquitto.org')
mqtt_client.connect()
print("MQTT connected!")

def handle_command(topic, message):
  payload = json.loads(message.decode())
  print("Message received:", payload)

  if payload['led_on']:
    led.on()
  else:
    led.off()

mqtt_client.set_callback(handle_command)
mqtt_client.subscribe(server_command_topic)

while True:
  light = light_sensor.read()
  telemetry = json.dumps({'light' : light})
  
  print("Sending telemetry ", telemetry)

  mqtt_client.publish(client_telemetry_topic, telemetry)

  mqtt_client.wait_msg()
    
  time.sleep(5)
