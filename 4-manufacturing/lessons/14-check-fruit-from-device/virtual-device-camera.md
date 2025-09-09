# Capture an image - Virtual IoT device

In the following lessons, you will add a camera sensor to an IoT device and read images from it. Due to the lack of available cameras for the ESP32 device, you will now use a Virtual IoT device instead. The first part of this guide will help you set up the virtual IoT device environment.

## Setup a virtual IoT device

Instead of purchasing an IoT device, along with sensors and actuators, you can use your computer to simulate IoT hardware. The [CounterFit project](https://github.com/CounterFit-IoT/CounterFit) allows you to run an app locally that simulates IoT hardware such as sensors and actuators, and access the sensors and actuators from local Python code that is written in the same way as the code you would write for real physical hardware, as Raspberry Pi for example.

### Task - install CounterFit

Install the Pip packages for CounterFit in your computer system or virtual machine.

1. From your terminal or command line, run the following commands to install the Pip packages for CounterFit. These packages include the main CounterFit app as well as shims for Grove hardware. These shims allow you to write code as if you were programming using physical sensors and actuators from the Grove ecosystem but connected to virtual IoT devices.

    ```sh
    pip3 install CounterFit
    pip3 install werkzeug==2.2.2
    pip3 install counterfit-connection
    ```

### Task - connect the 'hardware'

You will run the CounterFit app and connect your code to it. This is the virtual equivalent of plugging in some IoT hardware to a dev kit.

1. From a terminal or command line, launch the CounterFit app with the following command:

    ```sh
    counterfit
    ```

   The app will start running in the terminal, but to create and configure virtual sensors and actuators, you should open it in your web browser using the following URL:

    ```url
    http://127.0.0.1:5000
    ```

    ![The Counter Fit app running in a browser](../../../images/counterfit-first-run.png)

    It will be marked as *Disconnected*, with the LED in the top-right corner turned off.

1. **The `counterfit` process running in the terminal or command line should not be stopped, as the Virtual IoT devices need to communicate with it.**

## Hardware

The virtual IoT device will use a simulated camera that sends either images from files, or from your webcam.

### Add the camera to CounterFit

To use a virtual camera, you need to add one to the CounterFit app

#### Task - add the camera to CounterFit

Add the Camera to the CounterFit app.

1. Create a new Python file `app.py` on your computer in a folder called `fruit-quality-detector`. From now on, this file will simulate your IoT device.

1. Install an additional Pip package to install a CounterFit shim that can talk to Camera sensors by simulating some of the [Picamera Pip package](https://pypi.org/project/picamera/).

    ```sh
    pip3 install counterfit-shims-picamera
    ```

1. Make sure that the CounterFit instance is active in the terminal or command line, and that the web interface is accessible.

1. Create a camera:

    1. In the *Create sensor* box in the *Sensors* pane, drop down the *Sensor type* box and select *Camera*.

    1. Set the *Name* to `Picamera`

    1. Select the **Add** button to create the camera

    ![The camera settings](../../../images/counterfit-create-camera.png)

    The camera will be created and appear in the sensors list.

    ![The camera created](../../../images/counterfit-camera.png)

## Program the camera

The virtual IoT device can now be programmed to use the virtual camera.

### Task - program the camera

Program the device.

1. Open the `fruit-quality-detector` folder in VS Code or any code editor of your choice.

1. Open the `app.py` file.

1. Add the following code to the top of `app.py` to connect the app to CounterFit:

    ```python
    from counterfit_connection import CounterFitConnection
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

    This code imports the `CounterFitConnection` class from the `counterfit_connection` module, which comes from the `counterfit-connection` pip package you installed earlier. It then initializes a connection to the CounterFit app running on `127.0.0.1`, which is an IP address you can always use to access your local computer (often referred to as *localhost*), on port 5000.

    > 💁 If you have other apps running on port 5000, you can change this by updating the port in the code, and running CounterFit using `CounterFit --port <port_number>`, replacing `<port_number>` with the port you want to use.

1. From a terminal or command line, run the following to run your Python app:

    ```sh
    python3 app.py
    ```

    Confirm that the status of CounterFit will change to **Connected** and that the LED lights up. This indicates that your code is communicating properly with CounterFit.

    ![Counter Fit showing as connected](../../../images/counterfit-connected.png)

1. Add the following code to your `app.py` file:

    ```python
    import io
    from counterfit_shims_picamera import PiCamera
    ```

    This code imports some libraries needed, including the `PiCamera` class from the counterfit_shims_picamera library.

1. Add the following code below this to initialize the camera:

    ```python
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 0
    ```

    This code creates a PiCamera object, sets the resolution to 640x480. Although higher resolutions are supported, the image classifier works on much smaller images (227x227) so there is no need to capture and send larger images.

    The `camera.rotation = 0` line sets the rotation of the image in degrees. If you need to rotate the image from the webcam or the file, set this as appropriate. For example, if you want to change the image of a banana on a webcam in landscape mode to be portrait, set `camera.rotation = 90`.

1. Add the following code below this to capture the image as binary data:

    ```python
    image = io.BytesIO()
    camera.capture(image, 'jpeg')
    image.seek(0)
    ```

    This codes creates a `BytesIO` object to store binary data. The image is read from the camera as a JPEG file and stored in this object. This object has a position indicator to know where it is in the data so that more data can be written to the end if needed, so the `image.seek(0)` line moves this position back to the start so that all the data can be read later.

1. Below this, add the following to save the image to a file:

    ```python
    with open('image.jpg', 'wb') as image_file:
        image_file.write(image.read())
    ```

    This code opens a file called `image.jpg` for writing, then reads all the data from the `BytesIO` object and writes that to the file.

    > 💁 You can capture the image directly to a file instead of a `BytesIO` object by passing the file name to the `camera.capture` call. The reason for using the `BytesIO` object is so that later in this lesson you can send the image to your image classifier.

1. Configure the image that the camera in CounterFit will capture. You can either set the *Source* to *File*, then upload an image file, or set the *Source* to *WebCam*, and images will be captured from your web cam. Make sure you select the **Set** button after selecting a picture or selecting your webcam.

    ![CounterFit with a file set as the image source, and a web cam set showing a person holding a banana in a preview of the webcam](../../../images/counterfit-camera-options.png)

1. An image will be captured and saved as `image.jpg` in the current folder. You will see this file in the VS Code explorer. Select the file to view the image. If it needs rotation, update the `camera.rotation = 0` line as necessary and take another picture.

> 💁 You can find this code in the [code-camera/virtual-iot-device](code-camera/virtual-iot-device) folder.

😀 Your camera program was a success!
