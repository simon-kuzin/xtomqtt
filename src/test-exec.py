state={'dps':{
  '1':True,
  '12':"Some"
}}


globals={"state":state}
locals={"res":None}

code='''
dp1=state['dps']['1']
res="ON" if dp1 else "OFF"
'''

exec(code,globals,locals)

print(F"locals:{locals}")