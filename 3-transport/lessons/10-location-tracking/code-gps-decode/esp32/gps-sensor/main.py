import time

gpsDataFile = open('gpsDataFile.txt', 'r')

def convert_to_degree(rawData):
    deg = int(rawData/100)
    mins = rawData - float(deg*100)
    converted = float(deg + mins/60.0)
    return converted

def print_gps_data(data):
    data = data.strip()
    if 'GGA' in data:
        parts = data.split(',')
        lat = convert_to_degree(float(parts[2]))
        lon = convert_to_degree(float(parts[4]))
        
        if parts[3] == 'S':
            lat = lat * -1

        if parts[5] == 'W':
            lon = lon * -1

        print(f'{lat},{lon} - from {parts[7]} satellites')

while True:
    data = gpsDataFile.readline()
    if data:
        print_gps_data(data)
    else:
        print("End of file start again!!!")
        gpsDataFile.close()
        gpsDataFile = open('gpsDataFile.txt', 'r')
    time.sleep(1)