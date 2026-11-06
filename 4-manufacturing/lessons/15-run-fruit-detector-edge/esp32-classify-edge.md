# Classify an image using an IoT Edge based image classifier - ESP32

In this part of the lesson, you will use the Image Classifier running on the IoT Edge device.

## Use the IoT Edge classifier

The code is the same as in the previous lesson, except that the ESP32 now connects to your edge device using plain HTTP and the IP address or hostname of the computer running the IoT Edge inference server. No TLS is used, which also reduces memory usage on the ESP32.

### Task - use the IoT Edge classifier from the ESP32

1. Connect the ESP32 to the computer.

1. In Thonny, open the file from the previous lesson.
    
    > ⚠️ You can refer to the [instructions for calling the image classifier through Roboflow from project 4, lesson 14](../../../4-manufacturing/lessons/14-check-fruit-from-device/esp32-classify-image.md) if needed.

1. Change the following configuration to point at the IoT edge inference server:

    ```python
    host = '<HOST>'
	port = 9001
    ```

    Replace `<HOST>` with the IP address of the VM and make sure to set the port to 9001, which is used by the inference server.

1. Since the request uses plain HTTP without TLS, remove the following line from the classify function:

    ```python
    s = ssl.wrap_socket(s, server_hostname=HOST)
    ```

1. Make sure the IoT Edge device and the ESP32 are connected to the same network. Run your code on the ESP32. The output will be displayed in the console:

    ```output
    >>> %Run -c $EDITOR_CONTENT

    MPY: soft reboot
    connecting to network...
    network config: ('10.6.3.163', '255.255.240.0')
    unripe : 97.74 %
    ```

    > 💁 If you get a `MemoryError`, use a smaller image.

> 💁 You can find this code in the [code/esp32](code/esp32) folder.

😀 Your fruit quality classifier program was a success!