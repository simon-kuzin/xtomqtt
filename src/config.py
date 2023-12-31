import yaml,logging
from utils.collection import dict_slice_keys,dict_slice_not_keys

log = logging.getLogger(__name__)

mqtt_config=['client_id', 'clean_session', 'userdata', 'protocol', 'transport', 'reconnect_on_failure']

class Config:
  def __init__(self,filename='inventory.yml'):
    log.info("Loading configuration from %s",filename)
    with open(filename, 'r') as file:
        self.config_dict = yaml.safe_load(file)
  
  def get_devices(self):
   return self.config_dict["devices"]

  def get_mqtt_broker(self):
   return self.config_dict["mqtt"]["broker"]
  
  def get_mqtt_auth(self):
   return self.config_dict["mqtt"]["auth"]
  
  def get_mqtt_client_params(self):
    return dict_slice_keys(self.config_dict["mqtt"],mqtt_config)
