import socks
import socket
import requests
import port_scanner
import IPgenuce
import threading
import gc
import optparse
ports = [1973, 3128, 8741, 4195, 2500, 8080,8888, 1081, 1801, 9050, 9051, 4145,1080,8080,30169,34304,36975,37396,39323,41757,41928,42267,46928,49045,50483,52256,54973,61120,61219,9999]
results = []
File_NAME = "log.txt"
ADDRESS_WORK = '0.0.0.0'
def clean():
    j=[]
    for i in results:
        if i in j:
            continue
        j.append(i)
    return j
#range(1000,65537)
#, 1973, 8741, 4195, 2500, 8080, 1081, 1801, 9050, 9051
Socks_type = {'socks4' : socks.SOCKS4, 'socks5' : socks.SOCKS5, 'http' : socks.HTTP}
def set_old_socket():
    socket.socket = oldSocket
def set_new_socket(sockytype,ip,port,username=None,password=None):
    socks.set_default_proxy(sockytype,ip,port,True,username,password)
    socket.socket = socks.socksocket
def get_current_ip_address():
    try:
        return requests.get("http://icanhazip.com").content.decode('ascii')
    except:
        set_old_socket()
        return get_current_ip_address()
oldSocket = socket.socket
strMainIp = get_current_ip_address()
def get_new_Ip_Address(checkname=False,addr='0.0.0.0'):
    NewIpAddresshostname = None
    if checkname:
        while NewIpAddresshostname ==None:
            NewIpAddressip =IPgenuce.random_ip(addr)
            NewIpAddresshostname = IPgenuce.get_host_name(NewIpAddressip)
    else:
        NewIpAddressip =IPgenuce.random_ip(addr)
        NewIpAddresshostname = IPgenuce.get_host_name(NewIpAddressip)
    print("trying : ", NewIpAddresshostname, NewIpAddressip)
    return NewIpAddressip
def bloat_ip(Check,addrr='0.0.0.0'):
    yield get_new_Ip_Address(Check,addrr)
def scan_proxy(ip,port):
    #print("Trying",port)
    if port_scanner.verify_port(ip,port,time=1):
        results.append(str(ip)+" "+str(port)+" is open (Possibly Password Protected)")
    else:return
    if port == 8080:
        set_new_socket(socks.HTTP,ip,port)
        if get_current_ip_address() != strMainIp:
            results.append("New SOCKET FOUND: "+str(ip)+" "+str(port)+" HTTP")
        set_old_socket()
    else:
        set_new_socket(socks.SOCKS4,ip,port)
        if get_current_ip_address() != strMainIp:
            results.append("New SOCKET FOUND: "+str(ip)+" "+str(port)+" SOCKS4")
            set_old_socket()
            return
        set_new_socket(socks.SOCKS5,ip,port)
        if get_current_ip_address() != strMainIp:
            results.append(str("New SOCKET FOUND: "+str(ip)+" "+str(port)+" SOCKS5"))
        set_old_socket()
        return
def Scan_Ports(NewIpAddressip):
    k = []
    for port in ports:
        k.append(threading.Thread(target=scan_proxy,args=[NewIpAddressip,port]))
    for i in k:
        i.start()
    for i in k:
        i.join()
        i._delete()
def run(Checking_The_only):
    global results
    while 1:
        i=0
        for ip in bloat_ip(Checking_The_only,ADDRESS_WORK): 
            Scan_Ports(ip)
            results = clean()
            if len(results) > 0:
                for m in results:
                    open(File_NAME,'w').write(m+"\n")
                i+=len(results)
                print(i,"item/s found!")
            gc.collect()

if __name__ == '__main__':
    opt = optparse.OptionParser()
    opt.add_option('-c','--Check-Hostname',dest="check",action="store_true",help='Makes sure that the ip\'s has a hostname <default false>')
    opt.add_option('-s','--start-ip',dest="ipstar",help='the default start ip is <0.0.0.0> where zero marks where the change will be')
    opt.add_option('-l','--log-filename',dest="log",help='saves results to log file name <default log.txt>')

    options = opt.parse_args()[0]
    if(options.check):Checking_The_only=True
    else: Checking_The_only =False
    if options.ipstar != None: ADDRESS_WORK =options.ipstar
    if options.log != None: File_NAME=options.log
    run(Checking_The_only)
    