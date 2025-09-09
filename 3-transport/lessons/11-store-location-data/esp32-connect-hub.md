# Send GPS data to an IoT Hub - ESP32

In this part of the lesson, you will connect your ESP32 to your IoT Hub to send telemetry.

### Task - connect the ESP32 to the Internet and an IoT Hub

1. Connect the ESP32 to the computer.

1. In Thonny, open the file that contains the code from the previous lesson.

1. In this file, add the necessary code to connect your board to a Wi-Fi network.
    
    > ⚠️ You can refer to the [instructions to connect the ESP32 to the Internet from project 1, lesson 4](../../../1-getting-started/lessons/4-connect-internet/esp32-mqtt.md#task---connect-the-esp32-to-the-internet) if needed.

1. After that, add the relevant code to connect to the IoT Hub using the device SAS token you previously collected.

    > ⚠️ You can refer to the [instructions for connect your IoT device to IoT Hub from project 2, lesson 8](../../../2-farm/lessons/8-migrate-your-plant-to-the-cloud/esp32-connect-hub.md#task---connect-to-iot-hub) if needed.

### Task - send GPS data to an IoT Hub

In this part of the lesson, you will send GPS coordinates from a track to the IoT Hub. Since you don't have a real GPS device, you will use a [GPX](https://www.topografix.com/gpx.asp) file instead. This type of file is commonly used as a standard GPS data format in software applications. It uses an XML schema to store GPS coordinates, such as those from a recorded track.

Next, you will prepare your code to read each line of a GPX file, extract the latitude and longitude coordinates of each waypoint, and send them to an IoT Hub in the cloud. Since the latitude and longitude values in GPX files are already decoded, the decoding function will no longer be necessary.

1.  Download the following file [gpsTrack.gpx](code/gpsTrack.gpx), and save it to the ESP32 using Thonny.

1. Remove the `convert_to_degree` function, as it is no longer needed.

1. When you send the GPS data to the IoT Hub, do it as JSON in the following format:

    ```json
    {
        "gps" :
        {
            "lat" : <latitude>,
            "lon" : <longitude>
        }
    }
    ```
    So, import the `json` package into your code.

1. Since the GPX file uses a different format from NMEA sentences, the parsing logic must be adapted. Therefore, replace the contents of the `print_gps_data` function with the following:

    ```python
    data = data.strip()
    if 'trkpt lat=' in data:
        parts = data.split('"')
        lat = float(parts[1])
        lon = float(parts[3])
    ```
    > ⚠️ Take a look at the contents of the GPX file to better understand how the parsing logic works.

1. Now you can send GPS data to the IoT Hub. Add the following inside the `if` statement:

    ```python
    telemetry = json.dumps({ "gps" : {"lat" : lat, "lon" : lon}})
    print("Sending telemetry ", telemetry)
    device_client.send_telemetry(telemetry)
    ```

1. Finally, update the `open` function to read from the `gpsTrack.gpx` file you downloaded..

> 💁 You can find this code in the [code/esp32](code/esp32) folder.