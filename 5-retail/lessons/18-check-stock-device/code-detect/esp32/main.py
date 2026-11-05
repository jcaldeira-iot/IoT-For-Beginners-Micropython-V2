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
        print('%s:\t%.2f%%' % (p['class'], p['confidence'] * 100))
