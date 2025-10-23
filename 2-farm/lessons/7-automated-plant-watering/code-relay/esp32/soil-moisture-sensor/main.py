import time
from machine import ADC, Pin

adc = ADC(7, atten=ADC.ATTN_11DB)
relay = Pin(15, Pin.OUT)

while True:
    soil_moisture = adc.read()
    print("Soil moisture:", soil_moisture)

    if soil_moisture > 2047:
        print("Soil Moisture is too low, turning relay on (LED off).")
        relay.on()
    else:
        print("Soil Moisture is ok, turning relay off (LED on).")
        relay.off()
    
    time.sleep(2)
