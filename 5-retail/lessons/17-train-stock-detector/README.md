# Train a stock detector

![A sketchnote overview of this lesson](../../../sketchnotes/lesson-17.jpg)

> Sketchnote by [Nitya Narasimhan](https://github.com/nitya). Click the image for a larger version.

## Introduction

In the previous project, you used AI to train an image classifier - a model that can tell if an image contains something, such as ripe fruit or unripe fruit. Another type of AI model that can be used with images is object detection. These models don't classify an image by tags, instead they are trained to recognize objects, and can find them in images, not only detecting that the image is present, but detecting where in the image it is. This allows you to count objects in images.

In this lesson you will learn about object detection, including how it can be used in retail. You will also learn how to train an object detector in the cloud.

In this lesson we'll cover:

* [Object detection](#object-detection)
* [Use object detection in retail](#use-object-detection-in-retail)
* [Train an object detector](#train-an-object-detector)
* [Test your object detector](#test-your-object-detector)

## Object detection

Object detection involves detecting objects in images using AI. Unlike the image classifier you trained in the last project, object detection is not about predicting the best tag for an image as a whole, but for finding one or more objects in an image.

### Object detection vs image classification

Image classification is about classifying an image as a whole - what are the probabilities that the whole image matches each tag. You get back probabilities for every tag used to train the model.

![Image classification of cashew nuts and tomato paste](../../../images/image-classifier-cashews-tomato.png)

In the example above, two images are classified using a model trained to classify tubs of cashew nuts or cans of tomato paste. The first image is a tub of cashew nuts, and has two results from the image classifier:

| Tag            | Probability |
| -------------- | ----------: |
| `cashew nuts`  | 98.4%       |
| `tomato paste` | 1.6%        |

The second image is of a can of tomato paste, and the results are:

| Tag            | Probability |
| -------------- | ----------: |
| `cashew nuts`  | 0.7%        |
| `tomato paste` | 99.3%       |

You could use these value with a threshold percentage to predict what was in the image. But what if an image contained multiple cans of tomato paste, or both cashew nuts and tomato paste? The results would probably not give you what you want. This is where object detection comes in.

Object detection involves training a model to recognize objects. Instead of giving it images containing the object and telling it each image is one tag or another, you highlight the section of an image that contains the specific object, and tag that. You can tag a single object in an image or multiple. This way the model learns what the object itself looks like, not just what images that contain the object look like.

When you then use it to predict images, instead of getting back a list of tags and percentages, you get back a list of detected objects, with their bounding box and the probability that the object matches the assigned tag.

> 🎓 *Bounding boxes* are the boxes around an object.

![Object detection of cashew nuts and tomato paste](../../../images/object-detector-cashews-tomato.png)

The image above contains both a tub of cashew nuts and three cans of tomato paste. The object detector detected the cashew nuts, returning the bounding box that contains the cashew nuts with the percentage chance that the bounding box contains the object, in this case 97.6%. The object detector has also detected three cans of tomato paste, and provides three separate bounding boxes, one for each detected can, and each one has a percentage probability that the bounding box contains a can of tomato paste.

✅ Think of some different scenarios you might want to use image-based AI models for. Which ones would need classification, and which would need object detection?

### How object detection works

Object detection uses complex ML models. These models work by diving the image up into multiple cells, then checks if the center of the bounding box is the center of an image that matches one of the images used to train the model. You can think of this as kind of like running an image classifier over different parts of the image to look for matches.

> 💁 This is a drastic over-simplification. There are many techniques for object detection, and you can read more about them on the [Object detection page on Wikipedia](https://wikipedia.org/wiki/Object_detection).

There are a number of different models that can do object detection. One particularly famous model is [YOLO (You only look once)](https://pjreddie.com/darknet/yolo/), which is incredibly fast and can detect 20 different class of objects, such as people, dogs, bottles and cars.

✅ Read up on the YOLO model at [pjreddie.com/darknet/yolo/](https://pjreddie.com/darknet/yolo/)

Object detection models can be re-trained using transfer learning to detect custom objects.

## Use object detection in retail

Object detection has multiple uses in retail. Some include:

* **Stock checking and counting** - recognizing when stock is low on shelves. If stock is too low, notifications can be sent to staff or robots to re-stock shelves.
* **mask detection** - in stores with mask policies during public health events, object detection can recognize people with masks and those without.
* **Automated billing** - detecting items picked off shelves in automated stores and billing customers appropriately.
* **Hazard detection** - recognizing broken items on floors, or spilled liquids, alerting cleaning crews.

✅ Do some research: What are some more use cases for object detection in retail?

## Train an object detector

You can train an object detector using Roboflow, in a similar way to how you trained an image classifier.

> 💁 Roboflow has a free tier that is enough to create a model, train it, and use it for development work. Limits (number of images, training credits, and whether projects are public) change over time, so check the [Roboflow pricing page](https://roboflow.com/pricing) before starting, especially if you will use your own photos.

### Task - create an object detector

1. If you already created a Roboflow account and a workspace in the last project, you can use them again.

1. Go to [roboflow.com](https://roboflow.com) and sign in. If you don't have an account yet, create a free account and a workspace when prompted.

1. Select **Create New Project** and call the project `stock-detector`.

1. Set the project type to **Object Detection**.

✅ Take some time to explore the Roboflow UI for your object detector.

### Task - train your object detector

To train your model you will need a set of images containing the objects you want to detect.

1. Gather images that contain the object to detect. You will need at least 15 images containing each object to detect from a variety of different angles and in different lighting conditions, but the more the better. Try to set up the objects as if they were on a store shelf. You will also need a few images to test the model. If you are detecting more than one object, you will want some testing images that contain all the objects.

    > 💁 Images with multiple different objects count towards the 15 image minimum for all the objects in the image.

    Your images should be png or jpegs. The more images the better, and you should have a similar number of images of each object.

    The model is meant to be used for stock on shelves, so try to take the photos of the objects on shelves.

    You can find some example images that you can use in the [images](./images) folder of cashew nuts and tomato paste that you can use.

    > 💁 **Keep your test images separate.** Do not upload the test images to the project yet. You will use them later to check how the model behaves on images it has never seen.

1. Upload your training images to the project. Then annotate them: for each object, draw a bounding box and assign a class. Create the classes you need depending on the types of objects you want to detect, for example `cashew nuts` and `tomato paste`.

    When you draw bounding boxes for objects, keep them nice and tight around the object. It can take a while to outline all the images, but Roboflow has tools to speed this up, such as model-assisted labeling, which suggests boxes for you to confirm or correct.

    ![Tagging some cashew nuts](../../../images/object-detector-class-cashew.png)

    > 💁 If you have more than 15 images for each object, you can annotate the first images, then use the assisted labeling tools to suggest boxes on the remaining images. You can then confirm the detected objects, or reject and re-draw the bounding boxes. This can save a *lot* of time.

1. Start training from the version page using Roboflow's hosted training. You can choose an engine to train your model. To minimise training costs and time, select the **Custom Training** engine and a **Nano** model size with the **YOLO** architecture.

The object detector will then train. It will take a few minutes for the training to complete.

## Test your object detector

Once your object detector is trained, you can test it by giving it new images to detect objects in.

### Task - test your object detector

1. Open your trained model in the **Test** section and evaluate it using the images reserved for testing.

    ![3 cans of tomato paste detected](../../../images/object-detector-detected-tomato-paste.png)

1. Try all the testing images, ensuring that none were used for training, and observe the detected objects and their confidence scores.

1. Check how many objects of each class were found. Compare it with the number you can count in the image, because counting objects is the main use of an object detector in retail.

    > 💁 Object detectors usually let you set a *Confidence Threshold*, so that detections with a lower probability are ignored. Try changing it, and see how it changes the detections: a lower threshold finds more objects but also more false detections.

---

## 🚀 Challenge

What would happen if you used the object detector with similar looking items, such as same brand cans of tomato paste and chopped tomatoes?

If you have any similar looking items, test it out by adding images of them to your object detector.

## Review & Self Study

* When you trained your object detector, you would have seen values for *Precision*, *Recall*, and *mAP* that rate the model that was created. Read up on what these values are in the [Roboflow documentation](https://docs.roboflow.com) and on the [Object detection page on Wikipedia](https://wikipedia.org/wiki/Object_detection).
* Read more about object detection on the [Object detection page on Wikipedia](https://wikipedia.org/wiki/Object_detection)

## Assignment

[Compare domains](assignment.md)
