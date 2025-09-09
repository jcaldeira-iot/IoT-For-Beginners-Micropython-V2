# Connect your IoT device to the cloud - ESP32

In this part of the lesson, you will connect your ESP32 to your IoT Hub, to send telemetry and receive commands.

## Connect your device to IoT Hub

The next step is to connect your device to IoT Hub.

### Task - connect to IoT Hub

1. Connect the ESP32 to the computer.

1. Using Thonny open the file from the last lesson. You will be adding to this file.

1. Add the following imports to the file, below the code that connects to the Wi-Fi network:

    ```python
    try:
        import ioth
    except:
        import mip
        mip.install('github:jcaldeira-iot/iot-hub-micropython-client/package.json')
        import ioth
    from ioth import IoTHClient, IoTHEvents
    ```
    
   The `ioth` package will be installed from the [`GitHub repository`](https://github.com/jcaldeira-iot/iot-hub-micropython-client/) if it is not already present on the device. This package includes the SDK required to communicate with your IoT Hub.


1. Remove the `from umqtt.simple import MQTTClient` line as this library is no longer needed. Remove all the MQTT code including the topic names, all code that uses `mqtt_client` and the `handle_command`. Keep the `while True:` loop, just delete the `mqtt_client.publish` and `mqtt_client.wait_msg` lines form this loop.

1. Add the following code below the import statements:

    ```python
    iot_hub = '<hub_name>.azure-devices.net'
    device_id = 'soil-moisture-sensor'
    sas_token = '<sas_token>'
    ```

    Replace `<hub_name>` with your IoT hub name, replace `<sas_token>` with the SAS token you retrieved for the device earlier in this lesson (something like "SharedAccessSignature sr=...").

    > 💁 This is not best practice. Connection strings should never be stored in source code, as this can be checked into source code control and found by anyone. We are doing this here for the sake of simplicity.

1. Below this code, add the following to create a device client object that can communicate with IoT Hub, and connect it:

    ```python
    device_client = IoTHClient(iot_hub, device_id, sas_token)

    print('Connecting')
    device_client.connect()
    print('Connected')
    ```

1. Run this code. You will see your device connect.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    Connecting
    Device connected!
    Connected
    Sending telemetry {"soil_moisture": 3342}
    ```

## Handle commands

Your device needs to handle a command from the server code to control the relay. This is sent as a direct method request.

### Task - handle a direct method request

1. Add the following code before the `while True` loop:

    ```python
    def handle_method_request(request, ack):
        print("Direct method received - ", request.name)
    
        if request.name == "relay_on":
            relay.on()
        elif request.name == "relay_off":
            relay.off()
    ```

    This defines a method, `handle_method_request`, that will be called when a direct method is called by the IoT Hub. Each direct method has a name, and this code expects a method called `relay_on` to turn the relay on, and `relay_off` to turn the relay off.

    > 💁 This could also be implemented in a single direct method request, passing the desired state of the relay in a payload that can be passed with the method request and available from the `request` object.

1. Direct methods require a response to tell the calling code that they have been handled. Add the following code at the end of the `handle_method_request` function to create a response to the request:

    ```python
    ack(request, "200")
    ```

    This code sends a response to the direct method request with an HTTP status code of 200, and sends this back to the IoT Hub.

1. Add the following code below this function definition:

    ```python
    device_client.on(IoTHEvents.COMMANDS, handle_method_request)
    ```

    This code tells the IoT Hub client to call the `handle_method_request` function when a direct method is called.

## Send telemetry and listen to commands

After your device is connected, you can send telemetry to the IoT Hub and listen for incoming commands.

### Task - send telemetry and listen for incoming commands

1. Change the `while True:` loop as follows:

   ```python
   sec_count = 0
   while True:
       if sec_count == 0:
           soil_moisture = adc.read()
           telemetry = json.dumps({'soil_moisture' : soil_moisture})
           print("Sending telemetry ", telemetry)
           device_client.send_telemetry(telemetry)
       device_client.listen()
       sec_count = (sec_count + 1) % 10
       time.sleep(1)
   ```

   This code listens for incoming commands from the IoT Hub and sends a telemetry JSON string message every 10 seconds. The `cient.listen` function should be called in a polling manner (each 1s), so the `while` loop is adjusted to meet the timing requirements.

> 💁 You can find this code in the [code/esp32](code/esp32) folder.

😀 Your soil moisture sensor program is connected to your IoT Hub!
