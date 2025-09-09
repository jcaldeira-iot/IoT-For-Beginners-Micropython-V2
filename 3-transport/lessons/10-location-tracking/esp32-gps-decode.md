# Decode GPS data - ESP32

In this part of the lesson, you will decode the NMEA messages read from the GPS sensor by the ESP32, and extract the latitude and longitude.

## Decode GPS data

Once the raw NMEA data has been read from the file, it can be decoded.

### Task - decode GPS data

Program the device to decode the GPS data.

1. Connect the ESP32 to the computer.

1. In Thonny, open the file that contains the code for reading GPS data from the file.

1. Add the following function after the line that opens the file and before the `print_gps_data` function:

    ```python
    def convert_to_degree(rawData):
        deg = int(rawData/100)
        mins = rawData - float(deg*100)
        converted = float(deg + mins/60.0)
        return converted
    ```

1. Replace the contents of the `print_gps_data` function with the following:

    ```python
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
    ```

    This code begins by parsing the GPS data line read from the file.

    If the sentence contains [`GGA`](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm), it is a position fix message and will be processed. The latitude and longitude values are extracted from the message and converted to decimal degrees from the NMEA `(d)ddmm.mmmm` format.  The `convert_to_degree`function, previously added to the code, performs this conversion.

    The direction of the latitude is then checked, and if the latitude is south, then the value is converted to a negative number. Same with the longitude, if it is west then it is converted to a negative number.

    Finally the coordinates are printed to the console, along with the number of satellites used to get the location.

1. Save the file to the `MicroPython device` and run the code:

    The converted valeus of latitude and longitude from `GGA`sentences will be output to the `Shell` Thonny window.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    39.81902,-7.511981 - from 06 satellites
    39.81907,-7.511929 - from 06 satellites
    39.81905,-7.511972 - from 06 satellites
    ```

> 💁 You can find this code in the [code-gps-decode/esp32](code-gps-decode/esp32) folder.

😀 Your simulated GPS sensor program with data decoding was successful!
