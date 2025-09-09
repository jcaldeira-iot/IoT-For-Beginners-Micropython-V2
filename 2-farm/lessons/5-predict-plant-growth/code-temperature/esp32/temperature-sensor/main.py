import time
import dht

sensor = dht.DHT11(6)

while True:
    sensor.measure()
    temp = sensor.temperature()
    print(f'Temperature {temp}°C')
    time.sleep(10)
