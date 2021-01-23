import socket
from _thread import *
import json
import os
import sys
import time

address = ('127.0.0.1', 65432)

Serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Serv_sock.bind(address)
Serv_sock.listen(4)

print('Listening for connections on', address)

Conn_lst = []

msg = {"name":[], "message":[]}

# Function to serve as base for thread of every new client that connects
def User_Conn(SCK, ADDR):
    # Confirm client connection
    SCK.send("Welcome!".encode())

    end_time_user = time.time() + 180   # Time limit for thread exists without new messages

    while True:
        try:
            # Waiting for upcoming data
            # The data transmission from client
            # for server is made in a JSON file
            # here we convert the JSON back to python dict
            msg = json.loads(SCK.recv(2048).decode())

            print("Message:", msg["message"],", from:", ADDR, " at ", time.asctime(), sep='')   # Shows message on server console
            Update_Msg_History(msg, ADDR)   # Update the message historic
            SendFAll(SCK, msg) # Here we delivery the message from all the other connected clients

            if msg["message"] == 'exit':
                Close_conn(SCK)

            end_time_user = time.time() + 180
        except:
            if Exception:
                expt = sys.exc_info()
                update_log(expt)

            if time.time() > end_time_user:
                print('Inative client detected, closing connection')    # Closing an inactive connection
                Close_conn(SCK)
                break

            continue

# Function to deliver messages from all connected clients
# iterating through client list and sending message
# from those who aren't the sender instance
def SendFAll(Sender, msg):
    try:
        for Users in Conn_lst:
            if Users != Sender:
                Users.send(json.dumps(msg).encode())
    except Exception:
        expt = sys.exc_info()
        update_log(expt)

# Updating server log with raised exceptions
# to facilitate debug process
def update_log(Excpt):
    try:
        with open('./server/log.txt', 'a+') as up_log:
            up_log.write(f'{str(Excpt)} in {time.asctime()}\n')# Write raised exception in log for
                                                               # simplify debugging
    except Exception:
        pass

# Keep a historic
# for received messages
def Update_Msg_History(Msg, ADDR):
    try:
        with open('./server/History.txt', 'a+') as up_Hist:
            up_Hist.write(f'{Msg["name"]}: {Msg["message"]} | From address: {ADDR} in {time.asctime()}\n')
    except Exception:
        expt = sys.exc_info()
        update_log(expt)
        pass

# Function to close the socket connection
# and remove the user from active client list
def Close_conn(User):
    try:
       if User in Conn_lst:  # Check for socket object in list of clients
            Conn_lst.remove(User)  # Remove the client disconnected from list
            User.close()  # Close connection
    except Exception:
        expt = sys.exc_info()
        update_log(expt)

# Thread function to accept new connections
# and start threads for handle each new connection
def Accept_Conn_thread():
    while True:
        conn_usr, address = Serv_sock.accept()  # Accepting upcoming connections and saving socket instance and address
        print('User connected on address:', address)  # Showing in console the address of user

        Conn_lst.append(conn_usr)  # List of instances of all connected clients to SendFAll function iterate
        print("Active connections:", len(Conn_lst))

        start_new_thread(User_Conn, (conn_usr, address))  # Here we start a new thread for every new client connected
                                                          # so the server can handle multiple connections at same
                                                          # time without pausing or stoping to answer one by one

try:
    os.mkdir('./server')    # Trying to make a directory to store
                            # server log and message historic
except:
    pass

log = open('./server/log.txt', 'w+')    # Creating the log file
log.close()

Hist = open('./server/History.txt', 'w+')   # Creating the historic file
Hist.close()

start_new_thread(Accept_Conn_thread, ())    # Start the thread that accept new connections

end_time = time.time() + 120    # Time limit for server stay open without connections

while True:
    if not Conn_lst and time.time() >= end_time:
        print("No users connected for long time, closing server")
        Serv_sock.close()
        break
    elif Conn_lst and time.time() >= end_time:
        end_time = time.time() + 120