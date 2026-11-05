# Call your object detector from your IoT device - ESP32

Once your object detector has been published as a workflow, it can be used from your IoT device.

## Copy the image classifier project

The majority of your stock detector is the same as the image classifier you created in a previous lesson.

### Task - copy the image classifier project

1. Connect the ESP32 to the computer.

1. Since you don’t have a real camera, you will instead copy the image you want to classify onto the ESP32’s file system. Use a small image because the ESP32 has limited memory. You can upload the image file using Thonny by selecting **View → Files**, right-clicking the image file, and choosing **Upload to /**.

1. In Thonny, create a new file.

1. Replicate the steps from [lesson 14 of the manufacturing project](../../../4-manufacturing/lessons/14-check-fruit-from-device/esp32-classify-image.md) to call the workflow with an image from the ESP32. The majority of this code will be re-used to detect objects.

   > 💁 Use the `<API_KEY>`, `<WORKSPACE>` and `<WORKFLOW_ID>` of the workflow that contains your **object detection** model, which you created in this lesson, and not the workflow of the image classifier.

## Change the code from a classifier to an image detector

The code you used to classify images is very similar to the code to detect objects. The main difference is the model that the workflow runs, and the results of the call.

### Task - change the code from a classifier to an image detector

1. Remove the lines of code at the end of your file that process the results of the classifier:


   ~~pred = result["outputs"][0]["predictions"]~~  
   ~~print(pred["top"], ":", round(pred["confidence"] * 100, 2),"%")~~


1. Add the following function immediately after the call to the `classify` function. It will extract the detected objects from the workflow response:

   ```python
   def find_predictions(d):
       # Looks for the list of detections, which can be empty
       if isinstance(d, dict):
           p = d.get('predictions')
           if isinstance(p, list) and (not p or 'class' in p[0]):
               return p
           d = list(d.values())
       for v in d:
           if isinstance(v, (dict, list)):
               r = find_predictions(v)
               if r is not None:
                   return r
   ```

   An object detector can find no objects at all, so this version of the function also accepts an empty list.
   
1. Add the following code at the end of the file to detect the objects in the image:

   ```python
   result = classify(image_path)
   predictions = find_predictions(result)
   if predictions is None:
       print(result)
   else:
       threshold = 0.3
       detections = [p for p in predictions if p['confidence'] > threshold]
       for p in detections:
           print('%s:\t%.2f%%' % (p['class'], p['confidence'] * 100))
   ```

   This code sends the image to the workflow, which runs the object detector. It then gathers all the detections with a probability above a `threshold`, printing them to the console. If the reply has an unexpected structure, the full reply is printed instead, so you can see what was returned.

   Unlike an image classifier that only returns one result per class, the object detector will return multiple results, one for each object it finds, so any with a low probability need to be filtered out.   

1. Run this code and it will send the image to the object detector, and print out the detected objects.

   ```output
   cashew nuts:	   98.99%
   tomato paste:   91.42%
   tomato paste:   88.95%
   tomato paste:   87.05%
   tomato paste:   62.80%
   ```

   > 💁 You may need to adjust the `threshold` to an appropriate value for your images. The probabilities depend on your model and on your images.

   Each detection also contains the position of the object in the image, as `x`, `y`, `width` and `height`. You will use these values in the next part of the lesson.

   To compare the results with what your model sees, you can upload the same image to the testing tool of your model in Roboflow, and check the detections drawn on the image.

   > 💁 If you get a `MemoryError`, use a smaller image.

> 💁 You can find this code in the [code-detect/esp32](code-detect/esp32) folder.

😀 Your stock counter program was a success!