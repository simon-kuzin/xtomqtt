from utils import collection
import json, yaml , logging
from .feature import Entity,Feature
from .common import MQTT_ROOT
from drivers import tinytuya_driver



class MqttDevice:
  def __init__(self,device_id,config):
    self.id=device_id
    self.config=config
    self.log = logging.getLogger(F'MqttDevice:{ self.id}')
    self.availability_topic= F"{MQTT_ROOT}/{device_id}/availability"
    self.mqtt=None
    self.entities=[Entity(entity_id,entity_config,self,self.log) for entity_id,entity_config in config.get("entities").items()]
    self.device=tinytuya_driver.createDevice(self.id,self.config,self)
    
 
  def get_mqtt_config(self):
    return {
        "identifiers":[self.id,self.config.get("dev_id"),self.config.get("mac")],
        "name": self.config.get("name"),
        "sw_version" : self.config.get("version"),
        "manufacturer" :"Tuya",
        "suggested_area": self.config.get("area")
      }

  def onAvailability(self,isOnline):
    if self.mqtt:
      availability="online" if isOnline else "offline"
      self.mqtt.publish(self.availability_topic,availability,2,False)
      self.log.debug("Availability update published: %s",availability)
    else:
      self.log.warn("Availability update discarded. MqttClient not attached: %s",isOnline)

  def onState(self,state):
    for entity in self.entities:
      entity.onState(state)

  def mqtt_init(self,mqtt_client):
    self.mqtt=mqtt_client
    for entity in self.entities:
      entity.mqtt_init(mqtt_client)
  
  def start(self):
    return self.device.start(None)

  def stop(self):
    return self.device.stop()

  def on_command(self,entity,feature,message):
    self.log.info("Command received Device: %s Feature: %s/%s Command:%s",self.id,entity.id,feature.name,message)
    self.log.debug("Feature Config:%s",feature.config)
    self.device.on_command(entity,feature,message)