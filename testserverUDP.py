# -*- coding: utf-8 -*-
import socket
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(("127.0.0.1",19802))
while True:
    data,address = server.recvfrom(1024)
    server.sendto("udp server".encode('utf-8'),address)
print("done")
exit()
