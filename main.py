import socket
import sys
import select
import json

'''class Client:
    def __init__(self, UUID=None, message=None, name=None):
        self.UUID = UUID
        self.message = message
        self.name = name

    def update_UUID(self, n_UUID):
        self.UUID = n_UUID'''

Serv_addr = ('127.0.0.1', 65432)

print("Name: ")
name = input()

clnt_dict = {"Name":[], "UUID":[], "Message":[]}

clnt_dict["Name"] = name

while True:
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("You: ")
    clnt_dict["Message"] = input()

    try:
        if clnt_dict["UUID"] != []:
            data = json.dumps(clnt_dict)
            Client.connect(Serv_addr)
            Client.sendall(data.encode())
            data = Client.recv(2048).decode()
            msg = json.loads(data)
            Client.close()
            print(msg["Name"],":", msg["Message"])
            print(clnt_dict)
        else:
            data = json.dumps(clnt_dict)
            Client.connect(Serv_addr)
            Client.sendall(data.encode())
            data = Client.recv(2048).decode()
            msg = json.loads(data)
            clnt_dict["UUID"] = msg["UUID"]
            Client.close()
            print(clnt_dict)
    except:
        continue

    if (data == "sair"):
        Client.sendall(data)
        Client.close()
        break