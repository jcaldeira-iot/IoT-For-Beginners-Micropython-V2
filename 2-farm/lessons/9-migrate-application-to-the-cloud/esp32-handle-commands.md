# Handle commands from the cloud - ESP32

In this part of the lesson, you will change the code of your ESP32 so that it acts on the commands that your IoT service sends back in its replies, to control the relay.

## Handle commands from the IoT service

The function you wrote in this lesson answers every telemetry message with a command: `relay_on` if the plant needs watering, or `relay_off` if it doesn't. Your device needs to read this command and control the relay.

### Task - handle commands

1. Connect the ESP32 to the computer.

1. Using Thonny open the file from the last lesson, the one that sends telemetry to your IoT service. You will be adding to this file.

1. Add the following code before the `handle_reply` function:

    ```python
    def handle_command(command):
        print("Command received - ", command)

        if command == "relay_on":
            relay.on()
            time.sleep(20)
            relay.off()
        elif command == "relay_off":
            relay.off()
    ```

    This defines a function, `handle_command`, that is called with the command from the service. For `relay_on` it turns the relay on, waits for 20 seconds so the plant gets its water, and turns the relay off again. For `relay_off` it makes sure the relay is off.

    > 💁 The 20 second wait is done by the device, not by the function in the cloud. A function is short lived and stateless, so it cannot switch the relay on, wait, and then switch it off. Because the device also switches the relay off by itself, a network failure can never leave the relay on.

1. Replace the `handle_reply` function with the following:

    ```python
    def handle_reply(reply):
        command = reply.get('command')
        if command is not None:
            handle_command(command)
    ```

    This code looks at the reply from the service, and calls `handle_command` only if there is a command in it.

3. Run the code on your ESP32. Hold the sensor in the air or in water, and watch the output on the device and in the terminal of the service:

    ```output
     >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    Sending telemetry  {"soil_moisture": 3023}
    Command received -  relay_on
    Sending telemetry  {"soil_moisture": 1245}
    Command received -  relay_off
    ```

    The command you see depends on your soil moisture readings and on the threshold in your function.

> 💁 You can find this code in the [code/esp32](./code/esp32) folder.

😀 Your plant is now controlled by your IoT service!
