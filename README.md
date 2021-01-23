# Computer-Network-Project

This repository was created to store 
the codes of the final project of 
discipline of Computer Networks of 
Universidade Federal de Alagoas

<br>
Envolved students in this project:

- João Vitor Santos Tavares
- Rick Martim Lino dos Santos
<br>

The codes contained in this repository refer to the implementation of the client, server 
and client graphical interface.<br><br> 
The implemented application was a chat room 
based on the client-server architecture over the TCP transmission protocol, 
with a slight foundation in the communication 
model of applications such as Telegram and Whatsapp, 
which use the XMPP application protocol.<br><br> 
We do not use this protocol here, 
but we use a communication model using JSON, that is, 
something similar to an HTTP-based application architecture.

## How to run

To run the program download the .rar file and extract it. First run the server
and then run up to 4 clients (number used for convenience and can be changed on
server.py line 13 Serv_sock.listen(max number of connections)).

With the server running opens 2 or more clients, tipe your name on the login
screen and send messages from one to the other.

To send the messages press the "Enviar" button, when you decide to leave just
click "Sair" button at the botoom of the screen..

P.S.: Server is configured to shut down after 2 minutes without any connection.

## Why using JSON?

We are implementing a chat room, so we need to send some information to other customers, 
among which we have the recipient's name, 
your message, which are the ones we use in this code, 
but we could also have the sending time, date etc.

<br>
To avoid having to send several messages and generate more unnecessary 
traffic on the network, 
we send a JSON, 
whose format and type of file allows us to convert a 
Python object into a simple and easy to interpret structure.
<br><br>

![JSON Structure Example](https://d2tlksottdg9m1.cloudfront.net/uploads/2019/02/JSONSample.jpg)

<br>
In the case of our application, we use JSON to send a Python Dictionary from the client to the server and vice versa. Below is an example.

<br>

```python
import json
import socket

Addr = ('192.168.0.1', 54323)

my_dict = {"name":'Josias', "message":'Good morning everyone!'}

msg = json.dumps(my_dict)

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Client.connect(Addr)

Client.send(msg.encode())

msg = json.loads(Client.recv(1024).decode()) # We can also integrate the functions
                                             # like this
print(msg["name"],":",msg["message"],sep='')
```

<br>

In this example we use a client model to be able to demonstrate 
the use of JSON and its usefulness in our application.

<br>

## Threading

Threading here is also essential, it allows our server to 
continue servicing new connections while keeping old connections alive, 
without the need to keep renewing them.
<br>

Threading basically consists of making a program work so that it appears 
to have split up so that different parts 
of it can be run "at the same time". 
Below is an example of how the thread is used on our server.

```python
from _thread import *
import socket

Serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Conn_lst = []

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
```

<br>
Here we write a function to accept new connections within a main loop, 
whenever a new connection is generated 
start_new_thread is responsible for starting 
a thread from a function that will be 
responsible for handling requests from a given client.


<br><br>
And on the client we use thread to wait for new messages without the need to use the program's main loop, follow the example.

```python
import socket
from _thread import *

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
```
<Br>

## Error log and message history

Finally, we have implemented a simple error log and message history system, 
which consists of writing 
which errors or messages the client / server sends / receives
 and the Exceptions that may occur during their execution.

```python
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
```

<br>

Then that's it! 
Thanks for reading so far, have a great day and good studies!

![Carlton Dance](https://media.giphy.com/media/pa37AAGzKXoek/giphy.gif)

Goodbye! :)

[repository link](https://github.com/JT4v4res/Computer-Network-Project)

## References

- [Python Documentation - _Thread](https://docs.python.org/3/library/_thread.html)
- [Python Documentation - Time](https://docs.python.org/3/library/time.html#time.localtime)
- [Python Documentation - Tkinter](https://docs.python.org/3/library/tkinter.html?highlight=tkinter#module-tkinter)
- [Python Documentation - Socket](https://docs.python.org/3/library/socket.html?highlight=socket#module-socket)
- [Python Documentation - JSON](https://docs.python.org/3/library/json.html?highlight=json#module-json)
- [Python Documentation - Sys](https://docs.python.org/3/library/sys.html?highlight=sys#module-sys)
- [Python Documentation - Datetime](https://docs.python.org/3/library/datetime.html?highlight=datetime#module-datetime)
- [Python Documentation - Os](https://docs.python.org/3/library/os.html?highlight=os#module-os)