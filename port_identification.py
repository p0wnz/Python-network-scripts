import IPgenuce
import port_scanner
import bannergrabber
import requests
import threading
import socket
import gc
import optparse
logs = []
ports_open ={}
FILE_NAME=""
ports = [21,20,22,23,2222,24,25,53,67,68,69,76,80,110,111,123,137,138,139,143,161,162,173,389,443,636,989,990,3389,8080]
def clean_log(log):
    new_log=[]
    for logs in log:
        new_log.append(logs)
    return new_log
def scan_port_banner_grab(ip,port):
    global logs
    global ports_open
    ports_open = {}
    valid = port_scanner.verify_port(ip,port)
    if valid:
        if not port in [80,443,8080]: 
            logs.append("port open "+str(port))
            ports_open[port] = bannergrabber.banner_grab(ip,port)
            logs.append("port returned "+str(port)+": "+ports_open[port])
        elif port == 80 or port == 8080:
            
            content = requests.get("http://"+ip+":"+str(port)).content.decode("utf-8")
            if not '<HTML></HTML>' in content : 
                ports_open[port] = content
                logs.append("port returned "+str(port)+": "+content)
                logs.append("port open "+str(port))
                logs.append("port returned "+str(port)+": "+bannergrabber.banner_grab(ip,port))
        elif port == 443:
            ports_open[port] =requests.get("https://"+ip+":"+str(port)).content.decode("utf-8")
            logs.append("port open "+str(port))
            logs.append("port returned "+str(port)+": "+ports_open[port] )
            logs.append("port returned "+str(port)+": "+bannergrabber.banner_grab(ip,port))
        

def scan_port(FILE_NAME="",newIP="0.0.0.0",start_ip=None):
    global logs
    global ports_open
    ports_open={}
    i=0
    if newIP=="" :newIP = IPgenuce.random_ip(start_ip)
    #newIP = IPgenuce.random_ip_strong()
    logs.append("scanning "+newIP+" "+str(IPgenuce.get_host_name(newIP)))
    
    r = []
    for port in ports:
        r.append(threading.Thread(target=scan_port_banner_grab,args=[newIP,port]))
    for thread in r:
        thread.start()
    for thread in r:
        thread.join()
        thread._delete()
    while i < len(logs):
        logs=clean_log(logs)
        if FILE_NAME != "":
            for k in logs:  
                open(FILE_NAME).write(k+"\n")
        i+=1
    gc.collect()
ADDRESS_WORK="0.0.0.0"
ip=""
i=0
if __name__ == '__main__':
    opt = optparse.OptionParser()
    opt.add_option('-i','--ip-Address',dest="ip",help='Ip to scan default is to random ip')
    opt.add_option('-s','--start-ip',dest="ipstar",help='the default start ip is <0.0.0.0> where zero marks where the change will be')
    opt.add_option('-l','--log-filename',dest="log",help='saves results to log file name <default log.txt>')

    options = opt.parse_args()[0]
    if(options.ip != None): ip = options.ip
    if options.ipstar != None: ADDRESS_WORK =options.ipstar
    if options.log != None: File_NAME=options.log
    scan_port(FILE_NAME,ip,ADDRESS_WORK)
    
    for i in range(0,len(logs)):
        print(logs[i]+"\n")
    print("Scan Done")