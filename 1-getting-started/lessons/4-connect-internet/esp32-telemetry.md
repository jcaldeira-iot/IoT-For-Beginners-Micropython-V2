# Control your nightlight over the Internet - ESP32

In this part of the lesson, you will send telemetry with light levels from your ESP32 IoT device to an MQTT broker.

## Publish telemetry

The next step is to create a JSON document with telemetry and send it to the MQTT broker.

### Task

Publish telemetry to the MQTT broker.

1. Connect the ESP32 to the computer.

1. In Thonny, open the file that contains the nightlight code.

1. Add the following import to the top of the file:

    ```python
    import json
    ```

    The `json` library is used to encode the telemetry as a JSON document.

1. Add the following after the `client_name` declaration:

    ```python
    client_telemetry_topic = id + '/telemetry'
    ```

    The `client_telemetry_topic` is the MQTT topic the device will publish light levels to.

1. Replace the contents of the `while True:` loop at the end of the file with the following:

    ```python
    while True:
        light = light_sensor.read()
        telemetry = json.dumps({'light' : light})

        print("Sending telemetry ", telemetry)
    
        mqtt_client.publish(client_telemetry_topic, telemetry)
    
        time.sleep(5)
    ```

    This code packages the light level into a JSON document and publishes it to the MQTT broker. It then sleeps to reduce the frequency that messages are sent.

1. Run the code in the same way as you ran the code from the previous part of the assignment.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    MQTT connected!
    Sending telemetry  {"light": 3021}
    Sending telemetry  {"light": 3021}
    ```

> 💁 You can find this code in the [code-telemetry/esp32](code-telemetry/esp32) folder.

😀 You have successfully sent telemetry from your device.
