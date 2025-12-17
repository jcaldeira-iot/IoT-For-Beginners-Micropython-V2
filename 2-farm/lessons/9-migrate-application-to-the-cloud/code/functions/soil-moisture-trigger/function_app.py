import azure.functions as func
import datetime
import json
import logging

import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

app = func.FunctionApp()

@app.event_hub_message_trigger(
  arg_name="event",
  event_hub_name="",
  connection="IOT_HUB_CONNECTION_STRING"
)

def process_event(event: func.EventHubEvent):
  body = json.loads(json.loads(event.get_body().decode('utf-8')))
  device_id = event.iothub_metadata['connection-device-id']

  logging.info(f'Received message: {body} from {device_id}')
    
  soil_moisture = body['soil_moisture']

  if soil_moisture > 2047:
    direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
  else:
    direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')
    
  logging.info(f'Sending direct method request for {direct_method.method_name} for   device {device_id}')

  registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
  registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
    
  registry_manager.invoke_device_method(device_id, direct_method)

  logging.info('Direct method request sent!')
