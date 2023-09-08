from . import featureconfig
from utils import collection
import json, yaml , logging
from .common import MQTT_ROOT

log = logging.getLogger(__name__)


class Feature:
  def __init__(self,entity,name,config,log):
    self.log=log
    self.platform=entity.platform
    self.name=name
    self.entity=entity
    self.config=config
    entity_id=entity.id
    self.command_topic= F"{MQTT_ROOT}/{entity_id}/{name}/command" if "commands" in config else None
    self.state_topic= F"{MQTT_ROOT}/{entity_id}/{name}/state" if ("state" in config) & (config['state']!='None') else None
    self.oncommand_lambda=lambda client, userdata, message: self.on_command(message.payload.decode('utf-8'))
    self.last_state=None


  def get_mqtt_config(self):
    feature_config=getattr(featureconfig,self.name)
    print(self.name, feature_config)
    mqttconf={
      **(feature_config.get("defaults")),
      #**(self.config.get("properties"))
      }
      
    if self.state_topic:
      mqttconf[feature_config.get("state_topic")]=self.state_topic
    if self.command_topic:
      mqttconf[feature_config.get("command_topic")]=self.command_topic   
    return mqttconf
  
  def mqtt_init(self,mqtt_client):
    self.mqtt=mqtt_client
    if self.command_topic:
      mqtt_client.message_callback_add(self.command_topic,self.oncommand_lambda)
      mqtt_client.subscribe(self.command_topic,2)
      self.log.info("Subscribed to command feature:%s/%s topic:%s",self.entity.id, self.name, self.command_topic)
  
  def on_command(self,message):
    self.log.debug("Command Received. Feature %s, message: %s",self.name,message)
    self.entity.on_command(self,message)

  def onState(self,state):
    if self.state_topic is None:
        return None
    _globals={"state":state,"feature":self,"entity":self.entity}
    _locals={"msg":None}
    msg=None
    try:
      code=self.config['state']
      exec(code,_globals,_locals)
      msg=_locals['msg']
    except Exception:
      self.log.debug("Exception in calcullating state for feature %s",self.name,exc_info=True)
    if msg and (msg!=self.last_state) :
      self.mqtt.publish(self.state_topic,msg,2,True)
      self.log.info("Published State\ntopic:%s\nmessage: %s",self.state_topic,msg)
      self.last_state=msg

class Entity:
  def __init__(self,entity_id,config,device,log):
    self.platform=config.get("platform")
    self.config=config
    self.id=entity_id
    self.device=device
    self.features=[Feature(self,feat_id,feat_conf,log) for feat_id, feat_conf in config.get("features").items()]
    self.log=log
  
  def get_mqtt_config(self):
    conf={
      "availability_topic": self.device.availability_topic,
      "unique_id":self.id,
      "name": self.config.get("name"),
      "device":self.device.get_mqtt_config(),
      "payload_available":"online",
      "payload_not_available":"offline",
    }

    for feat in self.features:
      conf.update(feat.get_mqtt_config())  

    return collection.remove_null_values_recursive(conf) 

  def mqtt_init(self,mqtt_client):
    for feat in self.features:
      feat.mqtt_init(mqtt_client)
    
    mqtt_discovery_config=self.get_mqtt_config()
    mqtt_discovery_topic=F"homeassistant/{self.platform}/{self.id}/config"

    mqtt_client.publish(mqtt_discovery_topic,json.dumps(mqtt_discovery_config),2,True)
    self.log.info("Announced MQTT auto configuration\ntopic:%s\nconfig:\n%s",mqtt_discovery_topic,yaml.dump(mqtt_discovery_config))

  def on_command(self, feature,message):
    self.device.on_command(self,feature,message)

  def onState(self,state):
    for feat in self.features:
      feat.onState(state)