# Control your nightlight over the Internet - ESP32

The IoT device needs to be coded to communicate with *test.mosquitto.org* using MQTT to send telemetry values with the light sensor reading, and receive commands to control the LED.

In this part of the lesson, you will connect your ESP32 IoT device to an MQTT broker.

## Connect the ESP32 board to the Internet

Before communicating with the MQTT broker using the MQTT [micropython-lib](https://github.com/micropython/micropython-lib) package, you need to establish a network connection for your board.

### Task - Connect the ESP32 to the Internet

1. Connect the ESP32 to the computer.

1. In Thonny, open the file that contains the code from the previous lesson.

1. Add the following code to the begining of the file.

    ```sh
    import network

    ssid = '<NETWORK_SSID>'
    password = '<NETWORK_PASSWORD>'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ipconfig('addr4'))
    ```

    This code snippet connects your board to a wireless network. Replace `<NETWORK_SSID>` with the name of your network and `<NETWORK_PASSWORD>` with its password.

1. Save the file to the `MicroPython device` and run the code.

   The following output should be presented on the `Shell` Thonny window.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0') 
    Light level: 1034
    Light level: 1034
    Light level: 1034
    ```

## Code the device to connect to an MQTT broker

The device is ready to code.

### Task - Connect the ESP32 to an MQTT broker

Write the device code.

1. Add the following import after the previous code:

    ```python
    from umqtt.simple import MQTTClient
    ```

    The `umqtt.simple` library allows your board to communicate over MQTT.

1. Add the following code after the definitions of the light sensor and LED:

    ```python
    id = '<ID>'
    client_name = id + 'nightlight_client'
    ```

    Replace `<ID>` with a unique ID (e.g. your student number) that will be used the name of this device client, and later for the topics that this device publishes and subscribes to. The *test.mosquitto.org* broker is public and used by many people, including other students working through this assignment. Having a unique MQTT client name and topic names ensures your code won't clash with anyone elses. You will also need this ID when you are creating the server code later in this assignment.

    > 💁 You can use a website like [GUIDGen](https://www.guidgen.com) to generate a unique ID.

    The `client_name` is a unique name for this MQTT client on the broker.

1. Add the following code below this new code to create an MQTT client object and connect to the MQTT broker:

    ```python
    mqtt_client = MQTTClient(client_name, 'test.mosquitto.org')
    mqtt_client.connect()
    print("MQTT connected!")
    ```

    This code creates the client object and connects to the public MQTT broker.

1. Run the code in the same way as you ran the code from the previous part of the assignment.

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    MQTT connected!
    Light level: 1034
    Light level: 1034
    Light level: 1034
    ```

> 💁 You can find this code in the [code-mqtt/esp32](code-mqtt/esp32) folder.

😀 You have successfully connected your device to an MQTT broker.
