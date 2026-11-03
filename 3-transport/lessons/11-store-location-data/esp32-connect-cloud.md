# Send GPS data to an IoT service - ESP32

In this part of the lesson, you will connect your ESP32 to your IoT service to send telemetry.

### Task - connect the ESP32 to the Internet and an IoT service

1. Connect the ESP32 to the computer.

1. In Thonny, open the file that contains the code from the previous lesson.

1. In this file, add the necessary code to connect your board to a Wi-Fi network.

   > ⚠️ You can refer to the [instructions to connect the ESP32 to the Internet from project 1, lesson 4](../../../1-getting-started/lessons/4-connect-internet/esp32-mqtt.md#task---connect-the-esp32-to-the-internet) if needed.

1. After that, add the relevant code to connect to your IoT service using the device ID and the secret key you previously created.

   > ⚠️ You can refer to the [instructions for connecting your IoT device to the IoT service from project 2, lesson 8](../../../2-farm/lessons/8-migrate-your-plant-to-the-cloud/esp32-connect-cloud.md#task---connect-to-the-iot-service) if needed.

   Use the details of the new service you created in this lesson:

   ```python
   service_url = 'https://gps-sensor-iot.<your-subdomain>.workers.dev'
   device_id = 'gps-sensor'
   device_key = '<device key>'
   ```

   Replace `<your-subdomain>` with the one of your service, and `<device key>` with the secret key of the `gps-sensor` device. The `send_telemetry` function from that lesson is used here without any change.

### Task - send GPS data to an IoT service

In this part of the lesson, you will send GPS coordinates from a track to the IoT service. Since you don't have a real GPS device, you will use a [GPX](https://www.topografix.com/gpx.asp) file instead. This type of file is commonly used as a standard GPS data format in software applications. It uses an XML schema to store GPS coordinates, such as those from a recorded track.

Next, you will prepare your code to read each line of a GPX file, extract the latitude and longitude coordinates of each waypoint, and send them to your IoT service in the cloud. Since the latitude and longitude values in GPX files are already decoded, the decoding function will no longer be necessary.

1. Download the following file [gpsTrack.gpx](code/gpsTrack.gpx), and save it to the ESP32 using Thonny.

1. Remove the `convert_to_degree` function, as it is no longer needed.

1. When you send the GPS data to the IoT service, do it as JSON in the following format:

   ```
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

   ```
   data = data.strip()
   if 'trkpt lat=' in data:
        parts = data.split('"')
        lat = float(parts[1])
        lon = float(parts[3])
   ```

   > ⚠️ Take a look at the contents of the GPX file to better understand how the parsing logic works.

1. Now you can send GPS data to the IoT service. Add the following inside the `if` statement introduced in the previous step:

   ```
   telemetry = json.dumps({ "gps" : {"lat" : lat, "lon" : lon}})
   print("Sending telemetry ", telemetry)

   try:
        reply = send_telemetry(telemetry)
        print("Reply ", reply)
   except Exception as e:
        print("Error:", e)
   ```

   The service answers every message with a confirmation. If a request fails, for example because of a short Wi-Fi interruption, the error is printed and the device carries on with the next point.

1. Finally, update the `open` function to read from the `gpsTrack.gpx` file you downloaded.

1. Run the code. You will see each point being sent, and the confirmation from the service:

   ```output
   Sending telemetry  {"gps": {"lat": 39.81556, "lon": -7.48182}}
   Reply  {'status': 'received'}
   ```

   > 💁 If you get `HTTP 401: Unauthorized`, check that the `device_id` and `device_key` match the `gps-sensor` device you registered. If you get `HTTP 400`, the service did not find a numeric `gps.lat` and `gps.lon` in the telemetry, so check the JSON format.

   > 💁 Every point you send is stored in the later tasks of this lesson, and the free plan of the storage limits the number of writes to 1,000 a day. Make sure your code waits a few seconds between points, for example with `time.sleep(1)`, and avoid running the whole file over and over.

> 💁 You can find this code in the [code/esp32](code/esp32) folder.