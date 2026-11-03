import time

gpsDataFile = open('gpsDataFile.txt', 'r')

def print_gps_data(data):
    print(data.strip())

while True:
    data = gpsDataFile.readline()
    if data:
        print_gps_data(data)
    else:
        print("End of file!")
        gpsDataFile.close()
        break
    time.sleep(1)
