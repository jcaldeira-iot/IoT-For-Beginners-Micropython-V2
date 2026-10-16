# Classify an image - ESP32

In this part of the lesson, you will send an image stored on the ESP32 to the Roboflow service to classify it.

## Send images to Roboflow

Roboflow publishes your trained model as a *workflow* that you can call through a REST API. There is no Roboflow SDK for MicroPython, so your code will call the API directly over a network socket.

### Task - send images to Roboflow

1. Connect the ESP32 to the computer.

1. In Thonny, create a new file.

1. In this file, add the necessary code to connect your board to a Wi-Fi network.
    
    > ⚠️ You can refer to the [instructions to connect the ESP32 to the Internet from project 1, lesson 4](../../../1-getting-started/lessons/4-connect-internet/esp32-mqtt.md#task---connect-the-esp32-to-the-internet) if needed.

1. Since you don’t have a real camera, you will instead copy the image you want to classify onto the ESP32’s file system. Use a small image because the ESP32 has limited memory. You can upload the image file using Thonny by selecting **View → Files**, right-clicking the image file, and choosing **Upload to /**.

1. Add the following import statements at the top of the `app.py` file:

    ```python
    import gc
	import os
	import socket
	import ssl
	import ubinascii
	import ujson
    ```

    These modules provide network sockets and TLS for a secure connection, base64 encoding for the image, JSON parsing for the response, and file system access.

1. Add the following code to the end of the file:

    ```python
    host = '<HOST>'
	port = 443
	api_key = '<API_KEY>'
	workspace = '<WORKSPACE>'
	workflow_id = '<WORKFLOW_ID>'
	image_path = '<IMAGE_FILE_NAME>.png'
    ```

    Replace `<HOST>` with `serverless.roboflow.com`. Replace `<API_KEY>` with your Roboflow API key, and `<WORKSPACE>` and `<WORKFLOW_ID>` with the workspace name and the workflow ID of your fruit quality classifier. You can find the workspace name and workflow ID in the *Deploy* panel of your workflow in Roboflow. Replace `<IMAGE_FILE_NAME>` with the name of the image file to be classified.

    > ⚠️ Do not share your API key or publish it in a public repository.

5. The Roboflow API expects the image as base64 text inside a JSON body. Add the following code to build the address of your workflow and the fixed parts of the request body:

    ```python
    host_path = "/infer/workflows/%s/%s" % (workspace, workflow_id)
	start = b'{"inputs":{"image":{"type":"base64","value":"'
	end = b'"}}}'
    ```

    `host_path` is the address of your workflow on the server. `start` and `end` wrap the base64 image to form the JSON body. The name `image` must match the name of the image input of your workflow.

6. Create a function that sends the image to Roboflow with the following code:

    ```python
    def classify(path):
    	length = len(start) + (os.stat(path)[6] + 2) // 3 * 4 + len(end)

    	gc.collect()
	    s = socket.socket()
    	s.connect(socket.getaddrinfo(host, port)[0][-1])
	    s = ssl.wrap_socket(s, server_hostname=host)

    	s.write(("POST %s HTTP/1.0\r\nHost: %s\r\nAuthorization: Bearer %s\r\n"
             	 "Content-Type: application/json\r\nContent-Length: %d\r\n\r\n"
             	 % (host_path, host, api_key, length)).encode())
	    s.write(start)
    	with open(path, "rb") as f:
        	while True:
            	chunk = f.read(3 * 512)
	            if not chunk:
    	            break
        	    s.write(ubinascii.b2a_base64(chunk).strip())
	    s.write(end)

    	data = s.read()
	    s.close()
	    return ujson.loads(data.split(b"\r\n\r\n", 1)[1])
    ```

    This function opens a secure connection to Roboflow, sends the request headers, and then sends the image in small blocks, encoding each block to base64 as it goes. The ESP32 doesn't have enough memory to hold the whole encoded image at once, so it is never built in memory. The block size is a multiple of 3 so that the base64 encoding lines up between blocks. Finally the function reads the response, skips the HTTP headers, and converts the JSON body to a Python dictionary.

7. After this function, add the following code to send the image to Roboflow:

    ```python
    result = classify(image_path)
    ```

    This reads the image from the ESP32's file system and sends it to your workflow.

8. Finally, display the results filtered by the `class` and `confidence` fields in the JSON response using the following code:

    ```python
    pred = result["outputs"][0]["predictions"]
	print(pred["top"], ":", round(pred["confidence"] * 100, 2),"%")
    ```

> 💁 The response from a workflow can contain several outputs, if you want to print the full response instead, add the following instruction `print(result)`.

9. Run your code on the ESP32. You will see the output in the console:

    ```output
    unripe : 97.74 %
    ```

    > 💁 If you get a `MemoryError`, use a smaller image. If the request fails, check that the ESP32 is connected to Wi-Fi and that your API key, workspace name and workflow ID are correct.

> 💁 You can find this code in the [code/esp32](./code/esp32) folder.

😀 Your fruit quality classifier program was a success!