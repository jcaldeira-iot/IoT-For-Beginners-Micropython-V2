# IoT for Beginners - A Curriculum

Azure Cloud Advocates at Microsoft are pleased to offer 18-lesson curriculum all about IoT basics. Each lesson includes written instructions to complete the lesson, a solution, an assignment and more. Our project-based pedagogy allows you to learn while building, a proven way for new skills to 'stick'.

The projects cover the journey of food from farm to table. This includes farming, logistics, manufacturing, retail and consumer - all popular industry areas for IoT devices.

![A road map for the course showing 24 lessons covering intro, farming, transport, processing, retail and cooking](sketchnotes/Roadmap.jpg)

> Sketchnote by [Nitya Narasimhan](https://github.com/nitya). Click the image for a larger version.

**Hearty thanks to our authors [Jen Fox](https://github.com/jenfoxbot), [Jen Looper](https://github.com/jlooper), [Jim Bennett](https://github.com/jimbobbennett), and our sketchnote artist [Nitya Narasimhan](https://github.com/nitya).**

**Thanks as well to our team of [Microsoft Learn Student Ambassadors](https://studentambassadors.microsoft.com?WT.mc_id=academic-17441-jabenn) who have been reviewing and translating this curriculum - [Aditya Garg](https://github.com/AdityaGarg00), [Anurag Sharma](https://github.com/Anurag-0-1-A), [Arpita Das](https://github.com/Arpiiitaaa), [Aryan Jain](https://www.linkedin.com/in/aryan-jain-47a4a1145/), [Bhavesh Suneja](https://github.com/EliteWarrior315), [Faith Hunja](https://faithhunja.github.io/), [Lateefah Bello](https://www.linkedin.com/in/lateefah-bello/), [Manvi Jha](https://github.com/Severus-Matthew), [Mireille Tan](https://www.linkedin.com/in/mireille-tan-a4834819a/), [Mohammad Iftekher (Iftu) Ebne Jalal](https://github.com/Iftu119), [Mohammad Zulfikar](https://github.com/mohzulfikar), [Priyanshu Srivastav](https://www.linkedin.com/in/priyanshu-srivastav-b067241ba), [Thanmai Gowducheruvu](https://github.com/innovation-platform), and [Zina Kamel](https://www.linkedin.com/in/zina-kamel/).**

Meet the team!

[![Promo video](./images/IOT.gif)](https://youtu.be/-wippUJRi5k)

**Gif by** [Mohit Jaisal](https://linkedin.com/in/mohitjaisal)

> 🎥 Click the image above for a video about the project!

## Pedagogy

By the end of this series, students will have built a plant monitoring and watering system, a vehicle tracker, and a smart factory setup to track and check food, and will have learned the basics of the Internet of Things including how to write device code, connect to the cloud, analyze telemetry and run AI on the edge.

By ensuring that the content aligns with projects, the process is made more engaging for students and retention of concepts will be augmented. The projects start small and become increasingly more complex.

Each project is based around real-world hardware available to students and hobbyists. Each project looks into the specific project domain, providing relevant background knowledge. To be a successful developer it helps to understand the domain in which you are solving problems, providing this background knowledge allows students to think about their IoT solutions and learnings in the context of the kind of real-world problem that they might be asked to solve as an IoT developer. Students learn the 'why' of the solutions they are building, and get an appreciation of the end user.

> **[Students](https://aka.ms/student-page)**, to use this curriculum on your own, fork the entire repo and complete the exercises on your own, then reading the lecture and completing the rest of the activities. Try to create the projects by comprehending the lessons rather than copying the solution code; however that code is available in the /solutions folders in each project-oriented lesson. Another idea would be to form a study group with friends and go through the content together. For further study, we recommend [Microsoft Learn](https://docs.microsoft.com/users/jimbobbennett/collections/ke2ehd351jopwr?WT.mc_id=academic-17441-jabenn).

For an overview of this course, check out this video:

[![Promo video](https://img.youtube.com/vi/bccEMm8gRuc/0.jpg)](https://youtube.com/watch?v=bccEMm8gRuc "Promo video")

> 🎥 Click the image above for a video about the project!

## Each lesson includes:

- sketchnote
- optional supplemental video
- written lesson
- for project-based lessons, step-by-step guides on how to build the project
- knowledge checks
- a challenge
- supplemental reading
- assignment

## Lessons

|       |              Project Name              |                       Concepts Taught                       | Learning Objectives                                                                                                                                                 |                                                        Linked Lesson                                                         |
| :---: | :------------------------------------: | :---------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------: |
|  01   | [Getting started](./1-getting-started/README.md) |                     Introduction to IoT                     | Learn the basic principles of IoT and the basic building blocks of IoT solutions such as sensors and cloud services whilst you are setting up your first IoT device |                      [Introduction to IoT](./1-getting-started/lessons/1-introduction-to-iot/README.md)                      |
|  02   | [Getting started](./1-getting-started/README.md) |                   A deeper dive into IoT                    | Learn more about the components of an IoT system, as well as microcontrollers and single-board computers                                                            |                        [A deeper dive into IoT](./1-getting-started/lessons/2-deeper-dive/README.md)                         |
|  03   | [Getting started](./1-getting-started/README.md) | Interact with the physical world with sensors and actuators | Learn about sensors to gather data from the physical world, and actuators to send feedback, whilst you build a nightlight                                           | [Interact with the physical world with sensors and actuators](./1-getting-started/lessons/3-sensors-and-actuators/README.md) |
|  04   | [Getting started](./1-getting-started/README.md) |             Connect your device to the Internet             | Learn about how to connect an IoT device to the Internet to send and receive messages by connecting your nightlight to an MQTT broker                               |               [Connect your device to the Internet](./1-getting-started/lessons/4-connect-internet/README.md)                |
|  05   |            [Farm](./2-farm/README.md)            |                    Predict plant growth                     | Learn how to predict plant growth using temperature data captured by an IoT device                                                                                  |                          [Predict plant growth](./2-farm/lessons/5-predict-plant-growth/README.md)                           |
|  06   |            [Farm](./2-farm/README.md)            |                    Detect soil moisture                     | Learn how to detect soil moisture and calibrate a soil moisture sensor                                                                                              |                          [Detect soil moisture](./2-farm/lessons/6-detect-soil-moisture/README.md)                           |
|  07   |            [Farm](./2-farm/README.md)            |                  Automated plant watering                   | Learn how to automate and time watering using a relay and MQTT                                                                                                      |                      [Automated plant watering](./2-farm/lessons/7-automated-plant-watering/README.md)                       |
|  08   |            [Farm](./2-farm/README.md)            |               Migrate your plant to the cloud               | Learn about the cloud and cloud-hosted IoT services and how to connect your plant to one of these instead of a public MQTT broker                                   |               [Migrate your plant to the cloud](./2-farm/lessons/8-migrate-your-plant-to-the-cloud/README.md)                |
|  09   |            [Farm](./2-farm/README.md)            |         Migrate your application logic to the cloud         | Learn about how you can write application logic in the cloud that responds to IoT messages                                                                          |         [Migrate your application logic to the cloud](./2-farm/lessons/9-migrate-application-to-the-cloud/README.md)         |
|  10   |       [Transport](./3-transport/README.md)       |                      Location tracking                      | Learn about GPS location tracking for IoT devices                                                                                                                   |                           [Location tracking](./3-transport/lessons/10-location-tracking/README.md)                           |
|  11   |       [Transport](./3-transport/README.md)       |                     Store location data                     | Learn how to store IoT data to be visualized or analysed later                                                                                                      |                         [Store location data](./3-transport/lessons/11-store-location-data/README.md)                         |
|  12   |       [Transport](./3-transport/README.md)       |                   Visualize location data                   | Learn about visualizing location data on a map, and how maps represent the real 3d world in 2 dimensions                                                            |                     [Visualize location data](./3-transport/lessons/12-visualize-location-data/README.md)                     |
|  13   |   [Manufacturing](./4-manufacturing/README.md)   |               Train a fruit quality detector                | Learn about training an image classifier in the cloud to detect fruit quality                                                                                       |                 [Train a fruit quality detector](./4-manufacturing/lessons/13-train-fruit-detector/README.md)                 |
|  14   |   [Manufacturing](./4-manufacturing/README.md)   |           Check fruit quality from an IoT device            | Learn about using your fruit quality detector from an IoT device                                                                                                    |           [Check fruit quality from an IoT device](./4-manufacturing/lessons/14-check-fruit-from-device/README.md)            |
|  15   |   [Manufacturing](./4-manufacturing/README.md)   |             Run your fruit detector on the edge             | Learn about running your fruit detector on an IoT device on the edge                                                                                                |             [Run your fruit detector on the edge](./4-manufacturing/lessons/15-run-fruit-detector-edge/README.md)             |
|  16   |   [Manufacturing](./4-manufacturing/README.md)   |        Trigger fruit quality detection from a sensor        | Learn about triggering fruit quality detection from a sensor                                                                                                        |        [Trigger fruit quality detection from a sensor](./4-manufacturing/lessons/16-trigger-fruit-detector/README.md)         |
|  17   |          [Retail](./5-retail/README.md)          |                   Train a stock detector                    | Learn how to use object detection to train a stock detector to count stock in a shop                                                                                |                        [Train a stock detector](./5-retail/lessons/17-train-stock-detector/README.md)                         |
|  18   |          [Retail](./5-retail/README.md)          |               Check stock from an IoT device                | Learn how to check stock from an IoT device using an object detection model                                                                                         |                     [Check stock from an IoT device](./5-retail/lessons/18-check-stock-device/README.md)                      |

### Slides

There are slide decks for some of the lessons in the [slides](./slides) folder.

## Other Curricula

Our team produces other curricula! Check out:

- [AI for Beginners](https://aka.ms/ai-beginners)
- [Data Science for Beginners](https://aka.ms/datascience-beginners)
- [Generative AI for Beginners](https://aka.ms/genai-beginners)
- [**NEW** Cybersecurity for Beginners](https://github.com/microsoft/Security-101??WT.mc_id=academic-96948-sayoung)
- [Web Dev for Beginners](https://aka.ms/webdev-beginners?WT.mc_id=academic-113596-abartolo)
- [IoT for Beginners](https://aka.ms/iot-beginners)
- [Machine Learning for Beginners](https://aka.ms/ml-beginners)
- [XR Development for Beginners](https://aka.ms/xr-dev-for-beginners)
- [Mastering GitHub Copilot for AI Paired Programming](https://aka.ms/GitHubCopilotAI)

## Image attributions

You can find all the attributions for the images used in this curriculum where required in the [Attributions](./attributions.md).