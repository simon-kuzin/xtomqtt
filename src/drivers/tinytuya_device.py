from utils.collection import dict_slice_keys,dict_slice_not_keys
import tinytuya
from tinytuya import Contrib
from tinytuya.Contrib import RFRemoteControlDevice
from queue import PriorityQueue, Full, Empty
import logging,threading,yaml,time

COMMAND_PULL={"action":"pull"}
COMMAND_STOP={"action":"stop"}

device_exclude_keys=['type','name','mac','entities']
device_valid_params=['dev_id','address','local_key','version','connection_timeout','connection_retry_limit','dev_type','cid','node_id','parent']


def _device_constructor(deviceType):
  match  deviceType:
    case 'RFRemoteControlDevice':
      return RFRemoteControlDevice.RFRemoteControlDevice
    case _: 
      return tinytuya.OutletDevice

class TinytuyaDevice:

  def __init__(self,id,config,upstream):
    self.config=config
    self.id=id
    self.deviceType=config['type']
    self.device_params=dict_slice_keys(config,device_valid_params)
    self.queue=PriorityQueue(5)
    self.device=None
    self.log=logging.getLogger(F'tinytuya_driver:{self.id}')
    self.log.setLevel(logging.DEBUG)
    self.isOnline=False
    self.upstream=upstream
    self.thread=threading.Thread(target=self.run,daemon=True)

  def start(self,onStateChanged):
    self.log.debug("STARTING")
    self.enqueue_command(COMMAND_PULL,0)
    self.thread.start()

  def stop(self):
    self.log.debug("STOPPING")
    self.enqueue_command(COMMAND_STOP,0)
    self.thread.join()
  
  def on_command(self,entity,feature,message):
    self.log.info("Command received Device: %s Feature: %s/%s Command:%s",self.id,entity.id,feature.name,message)
    self.log.debug("Feature Config:%s",feature.config)
    command={'action':'execute'
              ,'command':{
                'entity':entity,
                'feature':feature,
                'message':message
                } 
            }
    self.enqueue_command(command)

  def enqueue_command(self,command,priority=10):
    try:
      self.log.debug("Queuing Command. command:%s priority:%s",command,priority)
      self.queue.put((priority,command),timeout=1)
    except Full: 
      self.log.warn("Queuing Command Failed. Queue full. command:%s priority:%s",command,priority)

  def execute_command(self,command):
    self.log.debug("Executing Command. command:%s",command)
    entity=command.get('entity')
    feature=command.get('feature')
    message=command.get('message')

    match command:
      case command if feature.name=='onoff':
        switch_no=feature.config.get('switch')
        if switch_no:
          self.device.set_status(message=="ON",switch_no)
        else:
          self.log.warning("Cannot execute command %s. Switch value is not configured in feature settings",command)
      case _:
          self.log.warning("Cannot execute command %s. Command is not supported",command)


  def onAvailability(self,isOnline):
    self.upstream.onAvailability(isOnline)

  def onState(self,state):
    self.upstream.onState(state)
    

  def run(self):
    self.log.debug("Device Thread Started")
    run=True
    while(run):
      commandToExecute=None
      try:
        command=self.queue.get(timeout=30)[1]
      except Empty:
        command=COMMAND_PULL
      

      match command['action']:
        case "pull" | None:
          pass
        case "stop" :
          break
        case _:
          commandToExecute=command
        
      try:
        if self.device is None:
          self.log.debug("Connecting type:%s params:%s",self.deviceType,yaml.dump(self.device_params))
          dev=_device_constructor(self.deviceType)(persist=True,connection_timeout=1,connection_retry_limit=1,connection_retry_delay=1,**self.device_params)
          self.device=dev
          #self.onAvailability(True)

        #TODO: execute command
        if commandToExecute:
          self.execute_command(commandToExecute['command'])

        state=self.device.status()
        dps=state.get('dps')
        self.log.debug("State :%s",state)
        self.onAvailability(True)
        if dps :
          self.onState(dps)
      except Exception as e:
        self.log.warn("Offline. Exception %s",e,exc_info=True)
        if commandToExecute:
          self.log.error("Command Failed:%s",commandToExecute)
        if self.device:
          del self.device
          self.device=None
        self.onAvailability(False)
      


      
