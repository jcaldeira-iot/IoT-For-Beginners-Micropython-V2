import network
import gc
import os
import socket
import ssl
import ubinascii
import ujson

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

host = '<HOST>'
port = 443
api_key = '<API_KEY>'
workspace = '<WORKSPACE>'
workflow_id = '<WORKFLOW_ID>'
image_path = '<IMAGE_FILE_NAME>.png'

host_path = "/infer/workflows/%s/%s" % (workspace, workflow_id)
start = b'{"inputs":{"image":{"type":"base64","value":"'
end = b'"}}}'

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

result = classify(image_path)

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

result = classify(image_path)
predictions = find_predictions(result)
if predictions is None:
    print(result)
else:
    threshold = 0.3
    detections = [p for p in predictions if p['confidence'] > threshold]
    for p in detections:
        print('%s:\t%.2f%%\tx=%.0f y=%.0f width=%.0f height=%.0f' % (p['class'], p['confidence'] * 100, p['x'], p['y'], p['width'], p['height']))

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

overlap_threshold = 0.20

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
draw_boxes(detections, 640, 480)
