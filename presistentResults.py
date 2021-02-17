import port_identification

while len(port_identification.ports_open.keys()) < 2:port_identification.scan_port()

print (port_identification.ports_open)