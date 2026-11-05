# Count stock from your IoT device - ESP32

A combination of the predictions and their bounding boxes can be used to count stock in an image

## Show bounding boxes

As a helpful debugging step you can not only print out the bounding boxes, but you can also draw them. An ESP32 cannot edit an image file, so you will draw them as a simple picture in the console instead.

Each detection returned by the object detector contains the position of the object as four values, measured in **pixels**: `x` and `y` are the position of the **center** of the bounding box, and `width` and `height` are its size. The origin (the 0,0 position) is the top left of the image.

### Task - print the bounding boxes

1. Connect the ESP32 to the computer.

1. Since you don’t have a real camera, you will instead copy the image you want to classify onto the ESP32’s file system. Use a small image because the ESP32 has limited memory. You can upload the image file using Thonny by selecting **View → Files**, right-clicking the image file, and choosing **Upload to /**.

1. In Thonny, open the file created in the previous step of this lesson.

1. Replace the `print` statement in the last `for` loop with the following code to display the bounding boxes data in the console:

   ```python
   print('%s:\t%.2f%%\tx=%.0f y=%.0f width=%.0f height=%.0f' % (p['class'], p['confidence'] * 100, p['x'], p['y'], p['width'], p['height']))
   ```
1. Run the app with an image of some stock on a shelf. The bounding boxes will be printed to the console, with the center position and the size in pixels.

   ```output
   >>> %Run -c $EDITOR_CONTENT

   MPY: soft reboot
   network config: ('10.6.3.162', '255.255.240.0')
   tomato paste:   93.42%  x=228 y=112 width=91 height=139
   tomato paste:   91.05%  x=330 y=116 width=76 height=130
   tomato paste:   88.27%  x=338 y=252 width=86 height=141
   tomato paste:   85.61%  x=236 y=261 width=92 height=136
   tomato paste:   41.20%  x=232 y=118 width=85 height=130
   ```

### Task - draw bounding boxes in the console

Image libraries such as Pillow are not available for MicroPython, so you will draw the boxes with text characters, on a grid that represents the image.

1. At the end of the file add the following two functions:

   ```python
   def clamp(value, low, high):
       return max(low, min(high, value))


   def draw_boxes(detections, image_width, image_height, columns=64, rows=24):
       grid = [[' '] * columns for _ in range(rows)]

       for p in detections:
           left = clamp(int((p['x'] - p['width'] / 2) / image_width * columns), 0, columns - 1)
           right = clamp(int((p['x'] + p['width'] / 2) / image_width * columns), 0, columns - 1)
           top = clamp(int((p['y'] - p['height'] / 2) / image_height * rows), 0, rows - 1)
           bottom = clamp(int((p['y'] + p['height'] / 2) / image_height * rows), 0, rows - 1)

           for c in range(left, right + 1):
               grid[top][c] = '-'
               grid[bottom][c] = '-'
           for r in range(top, bottom + 1):
               grid[r][left] = '|'
               grid[r][right] = '|'
           for r, c in ((top, left), (top, right), (bottom, left), (bottom, right)):
               grid[r][c] = '+'

       for row in grid:
           print(''.join(row).rstrip())
   ```

   This function creates a grid of 64 columns by 24 rows of spaces, which represents the image. For each detection, it calculates the left, right, top and bottom edges of the bounding box from the center position and the size. These values in pixels are converted to positions on the grid by dividing by the size of the image and multiplying by the number of columns or rows. For example, if the left edge is at 320 pixels on an image that is 640 pixels wide, then it is converted to column 32 (320 / 640 x 64 = 32). Each bounding box is then drawn with `-`, `|` and `+` characters, and the grid is printed.

   > 💁 The grid has fewer rows than columns because the characters in a console are about twice as tall as they are wide. With 64 columns and 24 rows, the picture has about the same proportions as an image that is 640 by 480 pixels.

1. Add the function calls immediately after the previously added functions:

   ```python
   draw_boxes(detections, 640, 480)
   ```

   Replace `640` and `480` with the width and height in pixels of the image you are using.

   > 💁 The reply from the object detector usually also contains the size of the image that was analyzed, in a value called `image`, with a `width` and a `height`. If you would prefer to read it from the reply, search the reply for it in the same way that `find_predictions` searches for the detections.

1. Run the app with an image of some stock on a shelf. You will see the bounding boxes drawn in the console.

   ```output
   >>> %Run -c $EDITOR_CONTENT

   MPY: soft reboot
   network config: ('10.6.3.162', '255.255.240.0')
                     +--------+ +------+
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     +--------+++--------+
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      +--------++--------+
   ```

   > 💁 The picture is only an approximation, but it is enough to check where the detector found the objects. To see the boxes on the real image, upload the same image to the testing tool of your model in Roboflow.

## Count stock

In the picture shown above, the bounding boxes have a small overlap. If this overlap was much larger, then the bounding boxes may indicate the same object. To count the objects correctly, you need to ignore boxes with a significant overlap.

### Task - count stock ignoring overlap

The overlap of two rectangles can be calculated with simple maths.

1. Before calling the `draw_boxes` function, add the following code:

   ```python
   overlap_threshold = 0.20
   ```

   This defines the percentage overlap allowed before the bounding boxes are considered to be the same object. 0.20 defines a 20% overlap.

1. To calculate the overlap, the center and size of each detection need to be converted into the edges of a box, and you need to be able to calculate the area of a box and of the overlap between two boxes. To do that add the following functions immediately before the calling the `draw_boxes` function:

   ```python
   def create_box(prediction):
       left = prediction['x'] - prediction['width'] / 2
       top = prediction['y'] - prediction['height'] / 2
       return (left, top, left + prediction['width'], top + prediction['height'])

   def box_area(box):
       return (box[2] - box[0]) * (box[3] - box[1])

   def overlap_area(box_1, box_2):
       width = min(box_1[2], box_2[2]) - max(box_1[0], box_2[0])
       height = min(box_1[3], box_2[3]) - max(box_1[1], box_2[1])
       if width <= 0 or height <= 0:
           return 0
       return width * height
   ```

   The `create_box` function creates a box with the left, top, right and bottom edges of the bounding box of a detection. The `overlap_area` function finds the part where two boxes cross, by looking at the right-most of the two left edges and the left-most of the two right edges (and the same for the top and bottom). If the boxes don't touch, the overlap is zero.

1. The logic for removing overlapping objects involves comparing all bounding boxes and if any pairs of detections have bounding boxes that overlap more than the threshold, delete one of the detections. To compare all the detections, you compare detection 1 with 2, 3, 4, etc., then 2 with 3, 4, etc. The following code performs this task, so add it immediately after the previously added functions:

   ```python
   to_delete = []

   for i in range(0, len(detections)):
       box_1 = create_box(detections[i])

       for j in range(i + 1, len(detections)):
           box_2 = create_box(detections[j])
           overlap = overlap_area(box_1, box_2)
           smallest_area = min(box_area(box_1), box_area(box_2))
           if overlap > (overlap_threshold * smallest_area):
               to_delete.append(detections[i])
               break

   for d in to_delete:
       detections.remove(d)

   print('Counted %d stock items' % len(detections))
   ```

   The overlap is calculated using the `overlap_area` function. This overlap threshold is not an absolute value, but needs to be a percentage of the bounding box, so the smallest bounding box is found, and the overlap threshold is used to calculate what area the overlap can be to not exceed the percentage overlap threshold of the smallest bounding box. If the overlap exceeds this, the detection is marked for deletion.

   Once a detection has been marked for deletion it doesn't need to be checked again, so the inner loop breaks out to check the next detection. You can't delete items from a list whilst iterating through it, so the bounding boxes that overlap more than the threshold are added to the `to_delete` list, then deleted at the end.

   Finally the stock count is printed to the console. This could then be sent to an IoT service to alert if the stock levels are low. All of this code is before the bounding boxes are drawn, so you will see the detections without overlaps in the picture.

   > 💁 This is very simplistic way to remove overlaps, just removing the first one in an overlapping pair. For production code, you would want to put more logic in here, such as considering the overlaps between multiple objects, or if one bounding box is contained by another.

1. Run the app with an image of some stock on a shelf. The output will indicate the number of bounding boxes without overlaps that exceed the threshold. Try adjusting the `overlap_threshold` value to see detections being ignored.

   ```output
   >>> %Run -c $EDITOR_CONTENT

   MPY: soft reboot
   network config: ('10.6.3.162', '255.255.240.0')
   tomato paste:   93.42%  x=228 y=112 width=91 height=139
   tomato paste:   91.05%  x=330 y=116 width=76 height=130
   tomato paste:   88.27%  x=338 y=252 width=86 height=141
   tomato paste:   85.61%  x=236 y=261 width=92 height=136
   tomato paste:   41.20%  x=232 y=118 width=85 height=130
   Counted 4 stock items
   
   
                     +--------+ +------+
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     |        | |      |
                     +--------+++--------+
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      |        ||        |
                      +--------++--------+
   ```

   In this example, five objects were detected, but the last one is almost on top of the first, so it was counted as the same can.

   > 💁 If you get a `MemoryError`, use a smaller image, and check that the workflow only returns the predictions as its output.

> 💁 You can find this code in the [code-count/esp32](code-count/esp32) folder.

😀 Your stock counter program was a success!