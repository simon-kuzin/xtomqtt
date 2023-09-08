def paho_connect_error(rc):
  match rc:
    case 0: return "Connection successful" 
    case 1: return "Connection refused - incorrect protocol version"
    case 2: return "Connection refused - invalid client identifier" 
    case 3: return "Connection refused - server unavailable" 
    case 4: return "Connection refused - bad username or password" 
    case 5: return "Connection refused - not authorised"
    case _: return "Unknown error"
