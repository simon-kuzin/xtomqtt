import coloredlogs, logging
import argparse
from config import Config
from inventory import Inventory
import paho.mqtt.client as mqtt


log = logging.getLogger("main")
coloredlogs.install(level='DEBUG',
                    fmt='%(asctime)s,%(msecs)03d %(levelname)-8s %(name)s : %(message)s'
                    )

paho_log = logging.getLogger("paho")
paho_log.setLevel(logging.INFO)

log.info("======= STARTING ======")


parser = argparse.ArgumentParser(
                    prog='X-To-MQTT',
                    )
parser.add_argument('filename') 
args=parser.parse_args()

config=Config(args.filename)
log.info("======= CONFIG LOADED ======")

inventory=Inventory(config.get_devices())
log.debug("Inventory created"
#, yaml.dump(inventory,default_flow_style=False)
)



def on_connect(client, userdata, flags, rc):
  if rc==mqtt.CONNACK_REFUSED_SERVER_UNAVAILABLE:
    log.warning(mqtt.connack_string(rc))
    return None
  elif rc!=mqtt.CONNACK_ACCEPTED:
    log.error(mqtt.connack_string(rc))
    client.disconnect()
    return None

  log.info("Connected to MQTT borker")
  inventory.mqtt_init(client)

  


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  log.warn("Unhandled MQTT Message received\ntopic:%s\npayload:%s\nqos:%s\nretain:%s", msg.topic,msg.payload,msg.qos,msg.retain)

client = mqtt.Client(**config.get_mqtt_client_params())
client.enable_logger(paho_log)
client.username_pw_set(**config.get_mqtt_auth())
client.on_connect = on_connect
client.on_message = on_message

inventory.start(client)

client.connect_async(**config.get_mqtt_broker())

try:
  client.loop_forever()
#except Exception as e:
 # log.error("Unhandled exception %s",e)
except SystemExit:
  log.info("SystemExit Initiated")
except KeyboardInterrupt:
  log.info("KeyboardInterrupt Initiated")
finally:
  log.info("======= STOPPING ======")
  inventory.stop()
