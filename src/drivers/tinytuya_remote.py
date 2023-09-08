from .tinytuya_device import TinytuyaDevice
from utils.collection import dict_slice_keys,dict_slice_not_keys


rf_send_button_params=['base64_code','times', 'delay', 'intervals']

class TinytuyaRemote(TinytuyaDevice):
  def __init__(self,id,config,upstream):
    super().__init__(id,config,upstream)

  def getMethodParams(self,entity,feature,message,expected_args):
    commands=feature.config['commands']
    cmd_config=commands.get(message,commands.get('default',{}))
    return dict_slice_keys(cmd_config,expected_args) 
  
  def execute_command(self,command):
    entity=command.get('entity')
    feature=command.get('feature')
    message=command.get('message')

    self.log.debug("TinytuyaRemote Executing Command. entity:%s feature:%s message:%s",entity, feature, message)
    if feature.config.get('commands') is None:
      self.log.warning("Commands are not configured for entity:%s feature:%s message:%s",entity.id,feature.name,message)
      return None
 
    match  self.deviceType:
      case 'RFRemoteControlDevice':
          kwargs=self.getMethodParams(entity,feature,message,rf_send_button_params)
          self.device.rf_send_button(**kwargs)
          dp=feature.config.get('dp')
          if dp:
            self.onState({'dps':{dp:message}})

      case _:
           self.log.warning("Commands for this deviceType are not supported. deviceType:%s",self.deviceType)

  def onState(self,state):
    if '201' not in state:
      super().onState(state)
    


