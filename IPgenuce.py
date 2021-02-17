import random
import sys
import socket
import optparse
def splice_ip_toint(ip):
    firstquart = int(ip.split('.')[0])
    secondquart = int(ip.split('.')[1])
    thridquart = int(ip.split('.')[2])
    fourthquart = int(ip.split('.')[3])
    return firstquart, secondquart, thridquart, fourthquart
def give_random_number(iprand):
    if(not iprand):
        return random.randrange(0,256)
    else: return iprand
def assemble_ip(ip1,ip2,ip3,ip4):
    return (str(ip1)+"."+str(ip2)+"."+str(ip3)+"."+str(ip4))
def random_ip(ip='0.0.0.0'):
    firstQuart , secondQuart, thirdQuart, fourthQuart = splice_ip_toint(ip)
    firstQuart = give_random_number(firstQuart)
    secondQuart = give_random_number(secondQuart)
    thirdQuart = give_random_number(thirdQuart)
    fourthQuart = give_random_number(fourthQuart)
    return assemble_ip(firstQuart,secondQuart,thirdQuart,fourthQuart)
def brute_ip(ipstar='0.0.0.0',ipend='255.255.255.255'):
    first ,second, third, fourth = splice_ip_toint(ipstar)
    while ipend != assemble_ip(first,second,third,fourth):
        if fourth > 255:
            fourth =0
            third +=1
        if third > 255:
            third=0
            second+=1
        if second > 255:
            second=0
            first+=1
        if first > 255:
            first = 0
        fourth +=1
        yield assemble_ip(first,second,third,fourth)    
    return
def get_host_name(ip):
    try:
        socket.setdefaulttimeout(1)
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None
def random_ip_strong():
    ip =random_ip()
    while get_host_name(ip) == None:ip =random_ip()
    return ip
if __name__ == '__main__':
    opt = optparse.OptionParser()
    opt.add_option('-r','--random',dest="random",action="store_true",help='This option chooses random ip\'s')
    opt.add_option('-b','--brute-force',dest="brute",action="store_true",help='This option BruteForces')
    opt.add_option('-s','--start-ip',dest="ipstar",help='the default start ip is <0.0.0.0> where zero marks where the change will be')
    opt.add_option('-e','--end-ip',dest="ipend",help='the default end ip is <255.255.255.255> <THIS OPTION IS ONLY VAILD WITH BRUTEFORCE>')
    if len(sys.argv ) <2:
        opt.print_help()
        exit()
    options = opt.parse_args()[0]
    if (options.random and options.brute) or (not options.random and not options.brute):
        opt.print_help()
        exit()
    elif(options.random):
        ipstar = options.ipstar
        if options.ipstar == None: ipstar ='0.0.0.0'
        while True:
            print(random_ip(ipstar))
    elif(options.brute):
        ipstar = options.ipstar
        ipend = options.ipend
        if options.ipstar == None: ipstar ='0.0.0.0'
        if options.ipend == None: ipend='255.255.255.255'
        for i in brute_ip(ipstar,ipend):
            print(i)
    else :
        opt.print_help()
        exit()