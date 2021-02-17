import socket
import sys
import optparse
def verify_address(IP_ADDRESS):
    try:
        socket.inet_aton(IP_ADDRESS)
        return IP_ADDRESS
    except socket.error:
        return socket.gethostbyname(IP_ADDRESS)
def verify_port(PORT):
    try:
        PORT = int(PORT)
        if PORT >0 and PORT < 65536:
            return True
        else: return False
    except:
        return False
def create_socket(IP_ADDRESS, PORT):
    sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
    IP_ADDRESS = verify_address(IP_ADDRESS)
    if not verify_port(PORT):
        print("INVAILD PORT NUMBER")
        exit()
    try:sck.connect((IP_ADDRESS,int(PORT)))
    except socket.timeout: return False
    except: return False
    return sck
def verify_integer(time):
    try:
        int(time)
        return True
    except:
        return False
def banner_grab(ipAddress, port, time=30, data="who are you"):
    banner = ''
    sck_main = create_socket(ipAddress,port)
    verify_integer(time)
    if not sck_main: return banner
    sck_main.settimeout(int(time))
    sck_main.send(data.encode('utf8'))
    try:
        banner = sck_main.recv(1024)
        banner = banner.decode('ascii')
    except socket.timeout:  return banner
    except: return banner
    sck_main.close()
    return banner
if __name__ == '__main__':
    ipAddress = ''
    port = 0
    opt = optparse.OptionParser()
    opt.add_option("-i",'--ip-address',dest='ipAddress',help='The ip address to grab the banenr from.<REQUIRED>')
    opt.add_option("-p",'--port',dest='port',help='The port to grab the banenr from.<REQUIRED>')
    opt.add_option("-t",'--time-out',dest='time',help='The amount of time to keep waiting for the server.<DEFUALT 5 SECONDS>')
    opt.add_option("-d",'--data',dest='data',help='The data to send.<DEFUALT \"who are you\"')
    if len(sys.argv) < 2:
        opt.print_help()
        exit()
    ipAddress = opt.parse_args()[0].ipAddress
    port = opt.parse_args()[0].port
    stime = opt.parse_args()[0].time 
    sdata = opt.parse_args()[0].data
    if stime == None and sdata == None:
        banner = banner_grab(ipAddress, port)
    elif stime != None and sdata == None:
        banner = banner_grab(ipAddress, port,time=stime)
    elif stime != None and sdata == None:
        banner = banner_grab(ipAddress, port,data=sdata)
    else:banner = banner_grab(ipAddress, port,data=sdata,time=stime)
    print(banner.decode('utf8'))