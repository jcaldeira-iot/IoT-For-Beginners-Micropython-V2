import time
from machine import ADC, Pin

light_sensor = ADC(5, atten=ADC.ATTN_0DB)
led = Pin(4, Pin.OUT)

while True:
  light = light_sensor.read()
  print('Light level:', light)
  if light < 2047:
    led.off()
  else:
    led.on()
    
  time.sleep(1)
