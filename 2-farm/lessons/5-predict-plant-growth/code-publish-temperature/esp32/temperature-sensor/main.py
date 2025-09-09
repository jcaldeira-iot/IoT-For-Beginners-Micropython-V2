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
import dht

sensor = dht.DHT11(6)

id = '<ID>'
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'

mqtt_client = MQTTClient(client_name, 'test.mosquitto.org')
mqtt_client.connect()
print('MQTT connected!')

while True:
  sensor.measure()
  temp = sensor.temperature()
  telemetry = json.dumps({'temperature' : temp})
  
  print('Sending telemetry:', telemetry)

  mqtt_client.publish(client_telemetry_topic, telemetry)
    
  time.sleep(10 * 60);
