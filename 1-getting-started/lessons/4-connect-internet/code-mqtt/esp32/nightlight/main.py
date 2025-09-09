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

mqtt_client = MQTTClient(client_name, 'test.mosquitto.org')
mqtt_client.connect()
print("MQTT connected!")

while True:
  light = light_sensor.read()
  print('Light level:', light)
  if light < 2047:
    led.off()
  else:
    led.on()
    
  time.sleep(1)
