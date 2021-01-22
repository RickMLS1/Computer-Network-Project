import socket
from _thread import *
import json
import sys
import time
import os

Serv_addr = ('127.0.0.1', 65432)

name = input(f'Name: ')

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Client.connect(Serv_addr)   # Connecting to server out of main loop so
                            # the client address and port are not changed

data = Client.recv(2048).decode()   # Receive server confirmation
print(data)

msg = {"name":[], "message":[]} # Dictionary def for JSON handle
msg["name"] = name

#Thread function to check for new messages and print then
def check_new_msg(Serv_conn):
    while True:
        try:    # Trying to receive new messages
            msg = json.loads(Serv_conn.recv(2048).decode())    # Converting from JSON to python dict

            if msg:
                print("\n",msg["name"],": ",msg["message"], sep='') # Showing the message received

                Update_Msg_History(msg)
        except Exception:
            expt = sys.exc_info()
            update_log(expt)
            continue

start_new_thread(check_new_msg, (Client, )) # Starting thread that checks for new messages

# Updating client log with raised exceptions
# to facilitate debug process
def update_log(Excpt):
    try:
        with open('./client/log.txt', 'a+') as up_log:
            up_log.write(f'{str(Excpt)} in {time.asctime()}\n')# Write raised exception in log for
                                                               # simplify debugging
    except Exception:
        pass

# Keep a historic
# for received messages
def Update_Msg_History(Msg):
    try:
        with open('./client/History.txt', 'a+') as up_Hist:
            up_Hist.write(f'{Msg["name"]}: {Msg["message"]} in {time.asctime()}\n')
    except Exception:
        expt = sys.exc_info()
        update_log(expt)
        pass

try:
    os.mkdir('./client')    # Trying to make a directory to store
                            # client log and message historic
except:
    pass

log = open('./client/log.txt', 'w+')    # Creating the log file
log.close()

Hist = open('./client/History.txt', 'w+')   # Creating the historic file
Hist.close()

while True:
    try:
        msg["message"] = input(f'You: ')

        if msg["message"] == 'exit': # if client wants to exit the chat room
            Client.send(json.dumps(msg).encode())
            Update_Msg_History(msg)
            msg = json.loads(Client.recv(2048).decode())
            print(msg["message"])
            Client.close()
            break

        Client.send(json.dumps(msg).encode())  # Conversion to python dict from JSON

    except Exception:
        expt = sys.exc_info()
        update_log(expt)
        Client.close()