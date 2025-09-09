# Read GPS data - ESP32

In this part of the lesson, you should add a GPS sensor to your ESP32 and read data from it.

## Hardware

The sensor you'll use is a [Grove GPS Air530 sensor](https://www.seeedstudio.com/Grove-GPS-Air530-p-4584.html). This sensor can connect to multiple GPS systems for a fast, accurate fix. The sensor is made of 2 parts - the core electronics of the sensor, and an external antenna connected by a thin wire to pick up the radio waves from the satellites.

![A grove GPS sensor](../../../images/grove-gps-sensor.png)

This is a UART sensor, so sends GPS data over UART.

## Connect the GPS sensor

Due to the limited availability of GPS sensors for this activity a file with simulated GPS data will be used. Reading data from this file will simulate the input from a real GPS sensor.

### Task - connect the GPS sensor

1. Connect the ESP32 to the computer.

1. Download the following file [gpsDataFile.txt](code-gps/gpsDataFile.txt), and save it to the ESP32 using Thonny.

## Program the GPS sensor

The ESP32 is now ready to be programmed to read GPS data from the downloaded file.

### Task - program the GPS sensor

Program the ESP32.

1. Using Thonny create a new file.

1. Add the following code to the file:

    ```python
    import time

    gpsDataFile = open('gpsDataFile.txt', 'r')

    def print_gps_data(data):
        print(data.strip())

    while True:
        data = gpsDataFile.readline()
        if data:
            print_gps_data(data)
        else:
            print("End of file! Start again...")
            gpsDataFile.close()
            gpsDataFile = open('gpsDataFile.txt', 'r')
        time.sleep(1)

    ```

    This code opens the GPS data file `gpsDataFile.txt` for reading `r`.

    Next a function called `print_gps_data` is defined that prints out the line passed to it to the console.

    Next, the code enters an infinite loop, reading one line of text from the file every second. It calls the `print_gps_data` function for each line. When the end of the file is reached, it closes and reopens the file to start again from the beginning.

1. Save the file to the `MicroPython device` and run the code.

    You will see the raw output from the GPS sensor (simulated), something like the following:

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    $GPRMC,143035.00,A,3949.14134,N,00730.71887,W,0.153,,010925,,,A*6B
    $GPVTG,,T,,M,0.153,N,0.283,K,A*2D
    $GPGGA,143035.00,3949.14134,N,00730.71887,W,1,06,1.55,383.4,M,49.3,M,,*4A
    $GPGSA,A,3,21,05,30,07,18,14,,,,,,,2.21,1.55,1.58*00
    $GPGSV,4,1,13,05,69,305,2,,,19,21,73,142,29,23,,,18,24,,,21*40
    $GPGSV,4,4,13,30,61,055,40*4B
    $GPGLL,3949.14134,N,00730.71887,W,143035.00,A,A*7A
    ```

> 💁 You can find this code in the [code-gps/esp32](code-gps/esp32) folder.

😀 Your simulated GPS sensor program was a success!
