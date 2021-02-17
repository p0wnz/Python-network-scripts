import proxyScanner
import optparse

def test_proxy(_type, ipaddress, port):
    failedBackIp = proxyScanner.get_current_ip_address()

    proxyScanner.set_new_socket(_type,ipaddress,port)

    if proxyScanner.get_current_ip_address() == failedBackIp: return False

    return True

def guess_proxy_by_guessing(ip, port):
    
    if (test_proxy(proxyScanner.Socks_type['socks4'], ip, port) == True):
        print(ip+':'+str(port)+" works on socks 4")
        exit()
    else:
        print(ip+':'+str(port)+' sock4 failed')
    if (test_proxy(proxyScanner.Socks_type['socks5'], ip, port) == True):
        print(ip+':'+str(port)+" works on socks 5")
        exit()
    else:
        print(ip+':'+str(port)+' sock5 failed')
    if (test_proxy(proxyScanner.Socks_type['http'], ip, port) == True):
        print(ip+':'+str(port)+" works on HTTP")
        exit()
    else:
        print(ip+':'+str(port)+' http failed')

if __name__ == "__main__":
    opt = optparse.OptionParser()
    opt.add_option('-i','--ip-address',dest="ip",help='the ip of the proxy')
    opt.add_option('-p','--port',dest="port",help='the port of the proxy')
    opt.add_option('-t','--type',dest="type_",help='give the type of proxy, (socks4, socks5, http)')

    options = opt.parse_args()[0]
    guess = False
    if options.ip == None: 
        print("provide an ip -i <ip>")
        exit()
    if options.port == None: 
        print("provide an a port -p <port>")
        exit()
    if options.type_ == None: guess = True
    if options.type_  != None and options.type_ != 'socks4' and options.type_ != 'socks5' and options.type_ != 'http':
        print("invaild proxy type, Supported proxys are socks4, socks5 and http")
        exit()


    if not guess:
        print('checking '+options.ip+':'+options.port+' on '+options.type_)
        if test_proxy(proxyScanner.Socks_type[options.type_], options.ip, int(options.port)):
            print("works")
        else:print("does not work")
    else: 
        print('guessing '+options.ip+':'+options.port+" Type")
        guess_proxy_by_guessing(options.ip, int(options.port))
    exit()