# Control your nightlight over the Internet - ESP32

In this part of the lesson, you will subscribe to commands sent from an MQTT broker to your ESP32 IoT device.

## Subscribe to commands

The next step is to subscribe to the commands sent from the MQTT broker and respond to them.

### Task

Subscribe to commands.

1. Connect the ESP32 to the computer.

1. In Thonny, open the file that contains the code from the previous lesson.

1. Add the following code after the definitions of the `client_telemetry_topic`:

    ```python
    server_command_topic = id + '/commands'
    ```

    The `server_command_topic` is the MQTT topic the device will subscribe to receive LED commands.

1. Add the following code just above the main loop, after the `mqtt_client.connect()` line:

    ```python
    def handle_command(topic, message):
        payload = json.loads(message.decode())
        print("Message received:", payload)
    
        if payload['led_on']:
            led.on()
        else:
            led.off()

    mqtt_client.set_callback(handle_command)
    mqtt_client.subscribe(server_command_topic)
    ```

    This code defines a function, `handle_command`, that reads a message as a JSON document and looks for the value of the `led_on` property. If it is set to `True` the LED is turned on, otherwise it is turned off.

    The MQTT client subscribes on the topic that the server will send messages on and sets the `handle_command` function to be called when a message is received.

1. Add the following instruction to the while loop, just before the `time.sleep(5)` line:

    ```python
    mqtt_client.wait_msg()
    ```
    This instruction waits for a message from the server.

1. Run the code in the same way as you ran the code from previous lessons.

1. Adjust the light levels detected by your sensor. Messages being received and commands being sent will be written to the terminal. The LED will also be turned on and off depending on the light level.

> 💁 You can find this code in the [code-commands/esp32](code-commands/esp32) folder.

😀 You have successfully coded your device to respond to commands from an MQTT broker.
