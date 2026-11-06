# Connect your IoT device to the cloud - ESP32

In this part of the lesson, you will connect your ESP32 to your IoT service, to send telemetry.

## Connect your device to the IoT service

The next step is to connect your device to the IoT service you deployed in this lesson.

### Task - connect to the IoT service

1. Connect the ESP32 to the computer.

1. Using Thonny open the file from the last lesson. You will be adding to this file.

1. Add the following imports to the file, below the code that connects to the Wi-Fi network and the device pins configuration:

    ```python
    import urequests as requests
    ```

    The `requests` library is used to send HTTPS requests to your IoT service. If it is not already present on the device, it will be installed from the package index.

1. Remove the `from umqtt.simple import MQTTClient` line as this library is no longer needed. Remove all the MQTT code including id, client name, topic names, all code that uses `mqtt_client` and the `handle_command` function. Keep the `while True:` loop, just delete the `mqtt_client.publish` and `mqtt_client.check_msg` lines from this loop.

1. Add the following code below the previous import statement:

    ```python
    service_url = 'https://soil-moisture-iot.<your-subdomain>.workers.dev'
    device_id = 'soil-moisture-sensor'
    device_key = '<device key>'
    ```

    Replace the `service_url` with the address of your IoT service that you noted when you deployed it, and replace `<device key>` with the secret key you generated for the device when you registered it earlier in this lesson.

    > 💁 This is not best practice. A secret key should never be stored in source code, as this can be checked into source code control and found by anyone. We are doing this here for the sake of simplicity.

1. Below this code, add the following function to send telemetry to the IoT service and return its reply:

    ```python
    def send_telemetry(telemetry):
        response = requests.post(
            service_url + '/telemetry',
            data=telemetry,
            headers={
                'Content-Type': 'application/json',
                'x-device-id': device_id,
                'x-api-key': device_key,
            },
        )
        try:
            if response.status_code != 200:
                raise RuntimeError('HTTP {}: {}'.format(response.status_code, response.text))
            return response.json()
        finally:
            response.close()
    ```

    The function sends a `POST` request to the `/telemetry` address of your service. The device ID and the secret key are sent in the headers, so the service can check that the device is registered. The reply from the service is returned as a Python dictionary.

1. Below this function, add the following code to test the connection:

    ```python
    print('Connecting')
    reply = send_telemetry(json.dumps({'soil_moisture': adc.read()}))
    print('Connected', reply)
    ```

1. Run this code. You will see your device connect.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    Connecting
    Connected {'status': 'received'}
    ```

    The service replies with a `status` of `received`, to confirm that it has accepted the telemetry.

    > 💁 If you get an error such as `HTTP 401: Unauthorized`, check that the `device_id` and `device_key` match the device you registered. If you get a network error, check that the ESP32 is connected to Wi-Fi and that the `service_url` is correct.

## Send telemetry and receive commands

After your device is registered, you can send telemetry to the IoT service and receive commands in the replies.

### Task - send telemetry and receive replies

1. Remove the test code you added in the previous task, the three lines that print `Connecting` and `Connected`.

1. Add the following function before the `while True:` loop:

    ```python
    def handle_reply(reply):
        print("Reply ", reply)
    ```

    This code prints the reply from the service

1. Change the `while True:` loop as follows:

    ```python
    while True:
        soil_moisture = adc.read()
        telemetry = json.dumps({'soil_moisture' : soil_moisture})
        print("Sending telemetry ", telemetry)

        try:
            reply = send_telemetry(telemetry)
            handle_reply(reply)
        except Exception as e:
            print("Error:", e)

        time.sleep(10)
    ```

    This code sends a telemetry JSON message every 10 seconds, and prints the reply from the service. If a request fails, for example because of a short Wi-Fi interruption, the error is printed and the loop carries on.

1. Run the code. You will see telemetry being sent every 10 seconds:

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    Sending telemetry  {"soil_moisture": 3342}
    Reply  {'status': 'received'}
    Sending telemetry  {"soil_moisture": 3320}
    Reply  {'status': 'received'}
    ```

> 💁 You can find this code in the [code/esp32](code/esp32) folder.

😀 Your soil moisture sensor program is connected to your IoT service!
