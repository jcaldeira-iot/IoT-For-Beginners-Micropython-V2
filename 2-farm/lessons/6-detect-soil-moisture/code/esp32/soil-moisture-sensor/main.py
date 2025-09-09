import time
from machine import ADC

adc = ADC(7, atten=ADC.ATTN_11DB)

while True:
    soil_moisture = adc.read()
    print("Soil moisture:", soil_moisture)
    
    time.sleep(1)
