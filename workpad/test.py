import tinytuya
from tinytuya import Contrib
from tinytuya.Contrib import RFRemoteControlDevice

"""
OUTLET Device
"""
#d = tinytuya.CoverDevice('bf82cbbf63f266a98b7g9p', '192.168.1.19', "196d1f7d92e6500a")
#d.set_version(3.3)
d = RFRemoteControlDevice.RFRemoteControlDevice( 'bf2991ef1de6cdbf89zluc', '192.168.1.11', "196d1f7d92e6500a",version="3.3",persist=True)

data = d.status()  

d.rf_send_button( "eyJudW0iOjEsInZlciI6IjIiLCJzdHVkeV9mZXEiOiI0MzMiLCJkYXRhMCI6IlRSOGFBZWtDK0FBTEEvZ0E2UUw0QUFzRCtBRHBBaG9CNlFMcEF2Z0E2UUlhQWZnQTZRTDRBQXNEK0FBTEF3c0QrQUFMQS9nQUN3UDRBT2tDR2dINEFPa0NHZ0hwQXZnQTZRTHBBdmdBK0FEcEFob0I2UUlMQS9nQStBRHBBdmdBQ3dQNEFBc0QrQURwQWhvQjZRSWFBZWtDK0FEcEFob0I2UUw0QU9rQ0dnSHBBdmdBIiwibHYiOlswXX0=", times=6, delay=0, intervals=0 )
#d.rf_send_button("eyJudW0iOjEsInZlciI6IjIiLCJzdHVkeV9mZXEiOiI0MzMiLCJkYXRhMCI6IlRCLzNBUElDOXdEeUFoa0I4Z0laQWZJQ0dRSHlBdmNBOGdMeUFoa0I4Z0wzQUJrQjhnTDNBUElDR1FIeUF2SUM5d0R5QXZjQThnTDNBUElDOXdEM0FQSUM5d0R5QXZjQThnTHlBdmNBOXdEeUF2Y0E4Z0x5QXZjQTl3RHlBaGtCOGdMM0FQSUM4Z0laQWZJQzl3RHlBaGtCOXdEeUF2SUM5d0R5QXZjQThnTDNBUGNBIiwibHYiOlswXX0=")
# Show status and state of first controlled switch on device
print('Dictionary %r' % data)
#print('State (bool, true is ON) %r' % data['dps']['1'])  

