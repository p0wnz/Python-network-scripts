import socket
import sys
import optparse

def verify_tcp(ip,port,data,time):    
    sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
    sck.settimeout(time)
    try:sck.connect((ip,port))
    except socket.timeout:
        return False
    except Exception as e:
        #print(e)
        return False
    sck.close()
    return True
def verify_udp(ip,port,data,time):
    sck = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sck.settimeout(time)
    try :
        sck.sendto(data.encode('utf-8'),0,(ip,port))
        newdata = sck.recv(1024).decode('utf-8')
        return newdata
    except socket.timeout:
        return False
    except Exception as e:
        if e == 'timed out':
            return False
        else:return False
def verify_port(ip,port,tcp=True,data="hello there",time=30):
    if tcp:return verify_tcp(ip,port,data,time)
    else:return verify_udp(ip,port,data,time)
if __name__ == '__main__':
    opt = optparse.OptionParser()
    opt.add_option('-i','--ip-address',dest="ip",help="The subjects ip address")
    opt.add_option('-p','--port',dest="port",help="The subjects port")
    opt.add_option('-u','--UDP',action='store_true',dest="udp",help="The subjects ip address<DEFUALT FALSE>")
    opt.add_option('-t','--timeout',dest="time",help="The subjects ip address<DEFAULT 3>")
    opt.add_option('-d','--data',dest="data",help="The data to be sent <DEFAULT: hello there>")
    options = opt.parse_args()[0]
    if options.ip == None or options.port == None:
        opt.print_help()
        exit()
    time = options.time
    if options.time == None: time = 30
    data = options.data
    if options.data == None: data = "hello there"
    udp = not options.udp
    if udp == None:
        udp = True
    print(verify_port(options.ip,int(options.port),udp,data=data,time=time))
