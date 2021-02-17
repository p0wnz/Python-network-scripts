# -*- coding: utf-8 -*-
import socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",19802))
conn = server.accept()
while True:
    data = server.recv(1024)
    server.send("TCP server".encode('utf-8'))
print("done")
exit()
