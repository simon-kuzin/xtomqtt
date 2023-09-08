import logging
from .tinytuya_device import TinytuyaDevice
from .tinytuya_remote import TinytuyaRemote

tinytuya_core_logger=logging.getLogger("tinytuya.core")
tinytuya_core_logger.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



def _device_constructor(deviceType):
  match  deviceType:
    case 'RFRemoteControlDevice':
      return TinytuyaRemote
    case _: 
      return TinytuyaDevice

#==============================================================================================
def createDevice(device_id, config,upstream):
  deviceType=config['type']
  return _device_constructor(deviceType)(device_id, config,upstream)



