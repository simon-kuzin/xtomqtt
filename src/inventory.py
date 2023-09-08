from mqtt_ha.mqttdevice import MqttDevice 
import coloredlogs, logging

log = logging.getLogger(__name__)

class Inventory:
  def __init__(self, devices_dict):
    self.devices=[MqttDevice(id,conf) for id,conf in devices_dict.items()]
  
  def mqtt_init(self,mqtt_client):
    for dev in  self.devices:
      dev.mqtt_init(mqtt_client)

    
  def start(self,mqtt_client):
    log.debug("STARTING Inventory")
    for dev in  self.devices:
      dev.start()

  def stop(self):
    log.debug("STOPPING Inventory")
    for dev in  self.devices:
      dev.stop()

#<discovery_prefix>/<component>/[<node_id>/]<object_id>/config

"""
devices = [
  Device(
    config={
      "~": "homeassistant/light/Kids-Light",
      "availability_topic": "~/availability",
      "unique_id":"Kids-Light",
      "name": "Kids Room Light",
      "command_topic":"~/switch",
      "state_topic":"~/state",
      "icon":"mdi:mdiCeilingFanLight",
      "device":{
        "identifiers":["Kids_Light"],
        "manufacturer":"Tuya",
        "suggested_area":"Kids Room"
      }
    }
  )
]
"""


  