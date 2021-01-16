import socket
import sys
import selectors
from _thread import *
import time
import random
import json

class Client:
    def __init__(self, UUID=None, message=None, name=None):
        self.UUID = UUID
        self.message = message
        self.name = name

    def update_UUID(self, n_UUID):
        self.UUID = n_UUID

address = ('127.0.0.1', 65432)
sel = selectors.DefaultSelector()

Serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Serv_sock.bind(address)
Serv_sock.listen(4)
#Serv_sock.settimeout(5)
print('Listeing on ', address)

Conn_lst = []

msg_tsnd = {"Name":[], "UUID":[], "Message":[]}
msg = {"Name":[], "UUID":[], "Message":[]}
#Conn_lst.append(conn_usr)

i = 1
while True:
    conn_usr, address = Serv_sock.accept()
    print('User connected on address:', address)

    #print('Active connections: ', len(Conn_lst))
    #print(Conn_lst)

    data = conn_usr.recv(2048).decode()
    msg = json.loads(data)

    if msg["UUID"] not in Conn_lst:
        msg["UUID"] = i
        Conn_lst.append(msg["UUID"])
        i += 1
        data = json.dumps(msg)
        conn_usr.sendall(data.encode())
    elif msg["UUID"] != msg_tsnd["UUID"]:
        data = json.dumps(msg_tsnd)
        conn_usr.sendall(data.encode())

    #print(msg["Message"], " UUID:" ,msg["UUID"])

    msg_tsnd = msg

    print("msg_tsnd content: ", msg_tsnd)

    '''data = 'Received!'
    conn_usr.sendall(data.encode())'''

    conn_usr.close()

    if msg == "sair":
        Serv_sock.close()
        break