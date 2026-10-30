# Connect your IoT device to the cloud - ESP32

In this part of the lesson, you will connect your ESP32 to your IoT service, to send telemetry and receive commands.

## Connect your device to the IoT service

The next step is to connect your device to the IoT service you deployed in this lesson.

### Task - connect to the IoT service

1. Connect the ESP32 to the computer.

2. Using Thonny open the file from the last lesson. You will be adding to this file.

3. Add the following import statement to the file, immediately after the code that connects to the Wi-Fi network and configures the device pins:

    ```python
    import urequests as requests
    ```

    The `requests` library is used to send HTTPS requests to your IoT service. If it is not already present on the device, it will be installed from the package index.

4. Remove the `from umqtt.simple import MQTTClient` line as this library is no longer needed. Remove all the MQTT code including id, client name, topic names, all code that uses `mqtt_client` and the `handle_command` function. Keep the `while True:` loop, just delete the `mqtt_client.publish` and `mqtt_client.check_msg` lines from this loop.

5. Add the following code below the previous import statement:

    ```python
    service_url = 'https://soil-moisture-iot.<your-subdomain>.workers.dev'
    device_id = 'soil-moisture-sensor'
    device_key = '<device key>'
    ```

    Replace the `service_url` with the address of your IoT service that you noted when you deployed it, and replace `<device key>` with the secret key you generated for the device when you registered it earlier in this lesson.

    > 💁 This is not best practice. A secret key should never be stored in source code, as this can be checked into source code control and found by anyone. We are doing this here for the sake of simplicity.

6. Below this code, add the following function to send telemetry to the IoT service and return its reply:

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

7. Below this function, add the following code to test the connection:

    ```python
    print('Connecting')
    reply = send_telemetry(json.dumps({'soil_moisture': adc.read()}))
    print('Connected', reply)
    ```

8. Run this code. You will see your device connect.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    Connecting
    Connected {'command': None}
    ```

    The `command` is `None` because there is no command waiting for the device.

    > 💁 If you get an error such as `HTTP 401: Unauthorized`, check that the `device_id` and `device_key` match the device you registered. If you get a network error, check that the ESP32 is connected to Wi-Fi and that the `service_url` is correct.

## Handle commands

Your device needs to handle a command from the IoT service to control the relay. The service sends it in the reply to the telemetry, and it is either `relay_on`, `relay_off`, or no command at all.

### Task - handle a command

1. Remove the test code you added in the previous task, the three lines that print `Connecting` and `Connected`.

1. Add the following code before the `while True` loop:

    ```python
    def handle_command(command):
        print("Command received - ", command)

        if command == "relay_on":
            relay.on()
        elif command == "relay_off":
            relay.off()
    ```

    This defines a function, `handle_command`, that will be called when the service sends a command. This code expects a command called `relay_on` to turn the relay on, and `relay_off` to turn the relay off.

    > 💁 The commands your service accepts are defined by the service. It only queues `relay_on` and `relay_off`, so the device does not need to handle anything else.

1. Add the following code below this function definition:

    ```python
    def handle_reply(reply):
        command = reply.get('command')
        if command is not None:
            handle_command(command)
    ```

    This code looks at the reply from the service, and calls `handle_command` only if there is a command in it. Unlike the previous lesson, the device doesn't need to confirm that it has handled the command, because the service removes it from the queue when it hands it over.

## Send telemetry and receive commands

After your device is registered, you can send telemetry to the IoT service and receive commands in the replies.

### Task - send telemetry and receive commands

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

    This code sends a telemetry JSON message every 10 seconds, and handles any command that comes back in the reply. If a request fails, for example because of a short Wi-Fi interruption, the error is printed and the loop carries on.

    > 💁 The device only receives a command when it sends telemetry, so a command you queue can take up to 10 seconds to reach it, plus a short delay for it to become visible in the service. This is different from the previous lesson, where the device listened for messages all the time.

1. Run the code. You will see telemetry being sent every 10 seconds:

    ```output
    Sending telemetry  {"soil_moisture": 3342}
    Sending telemetry  {"soil_moisture": 3320}
    ```

> 💁 You can find this code in the [code/esp32](./code/esp32) folder.

😀 Your soil moisture sensor program is connected to your IoT service!
