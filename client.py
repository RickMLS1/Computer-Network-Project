# coding=utf8
import socket
from _thread import *
import json
import sys
import time
import datetime as dt
import os
from tkinter import *


# Interface attribute values
color1 = "#560656"   # Purple
color2 = "white"
color3 = "#430543"   # Dark purple
color4 = "#262626"   # Dark grey
fonte  = 'Times 12'  # Font Times New Roman size: 12

Serv_addr = ('127.0.0.1', 65432)    # Defines Server Address

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    os.mkdir('./client')    # Trying to make a directory to store
                            # client log and message historic
except:
    pass

log = open('./client/log.txt', 'w+')    # Creating the log file
log.close()

Hist = open('./client/History.txt', 'w+')   # Creating the historic file
Hist.close()

msg = {"name":[], "message":[], "time":[]} # Dictionary def for JSON handle

# Updating client log with raised exceptions
# to facilitate debug process
def update_log(Excpt):
    try:
        with open('./client/log.txt', 'a+') as up_log:
            up_log.write(f'{str(Excpt)} in {time.asctime()}\n') # Write raised exception in log for
                                                                # simplify debugging
    except Exception:
        pass

# Keep a historic
# for received messages
def Update_Msg_History(Msg):
    try:
        with open('./client/History.txt', 'a+') as up_Hist:
            up_Hist.write(f'{Msg["name"]}: {Msg["message"]} in {time.asctime()}\n') # Writes received messages
                                                                                    # in a message historic
    except Exception:
        expt = sys.exc_info()
        update_log(expt)
        pass


# Function that exit the chat window
def logout_f(window):
    window.destroy()  #Closing chat window

    global msg
    msg["message"] = 'exit'

    Client.send(json.dumps(msg).encode())   # Send the close message for server end task and close socket
    Update_Msg_History(msg)

    Client.close()
    exit()


# Thread function to check for new messages and print then
def check_new_msg(Serv_conn, Chat_window):
    while True:
        try:    # Trying to receive new messages
            msg = json.loads(Serv_conn.recv(2048).decode())    # Converting from JSON to python dict

            if msg and msg != '\n' and msg != "" and msg != 'exit':
                #print("\n",, sep='') # Showing the message received
                if '\n' in msg:
                    show_msg = msg["time"] + " " + msg["name"] + ": " + msg["message"]
                else:
                    show_msg = msg["time"] + " " + msg["name"] + ": " + msg["message"]+'\n'

                Chat_window['state'] = NORMAL              # Changing state of the widget for its manipulation
                Chat_window.insert(END, show_msg)          # shows the message in the window text box
                Chat_window['state'] = DISABLED            # changing state of the widget for don't allow user
                                                           # local alteration in the output

                Update_Msg_History(show_msg)
        except Exception:
            expt = sys.exc_info()   # Catch Exception
            update_log(expt)    # Calls log
            continue


# Get user entry and shows new messages
def msg_send(mensagens, entry, username):
    user_entry = entry.get(1.0, 'end-1c')      # Get the user message from screen

    global msg

    if (user_entry != '\n' and user_entry != ""):
        msg["message"] = user_entry
        msg["time"] = str(dt.datetime.now().hour) + ":" + str(dt.datetime.now().minute)

        Client.send(json.dumps(msg).encode())                # Conversion to python dict from JSON
        new_message = (msg["time"]+ " " + username + ': ' + user_entry + '\n')  # Concatenating hour, message and user
        mensagens['state'] = NORMAL                          # changing state of widget for its manipulation
        mensagens.insert(END, new_message)                   # shows the message in the window text box
        mensagens['state'] = DISABLED                        # changing state of the widget for don't allow user
                                                             # local alterations in the output

        entry.delete(1.0, END)                               # Cleaning the entry text box


# Creation Function of the chat window
def chat(login_window, username):
    if username:                                      # Checks if the user provided the username entry
        msg["name"] = username

        login_window.destroy()                        # Closing the login's window

        # Window creation and assignment of its attributes
        chat_window = Tk()                            # Creating window
        chat_window['bg'] = color1                    # Background color
        chat_window.title('Chat')                     # Title
        chat_window.iconbitmap('./icons/chat_icon.ico')       # Icon
        centralize(chat_window, 756, 520)             # Call of the function that centralizes
                                                      # the established 756x520 window
        chat_window.resizable(False, False)           # Resizable property disable

        # Frame's creation
        framessage = Frame(chat_window, bg = color1)  # Creating and specifying its attributes

        # Widgets

        # Creating Text Box, that shows the messages from the users, and its attributes
        messages = Text(chat_window, font = fonte, height = 15, state = DISABLED, bg = color4, fg = color2)

        # Creating Text Box, for user input message, and its attributes
        entry = Text(framessage, height = 5, font = fonte, bg = color4, fg = color2)

        # Creating Submit Button, for send user message to the server, and its attributes
        submit = Button(framessage, bg = color3, fg = color2, font = fonte, text = 'Enviar',
                        command = lambda: msg_send(messages, entry, username))

        # Creating Exit Button, that exit this window, and its attributes
        logout   = Button (chat_window, bg = color3, fg = color2, font = fonte, text = 'Sair',
                           command = lambda: logout_f(chat_window))

        start_new_thread(check_new_msg, (Client, messages))  # Starting thread that checks for new messages
                                                             # and show then in screen

        # Placing the Frame and its widgets at specify positions of the window for building the interface
        framessage.grid (row = 1, column = 0, padx = 10, ipadx = 10, pady = 10, ipady = 10)
        messages.grid   (row = 0, column = 0, padx = 10, ipadx = 10, pady = 10, ipady = 10, sticky = 'we' )
        entry.grid      (row = 0, column = 0, padx = 10)
        submit.grid     (row = 0, column = 1)
        logout.grid     (row = 2, column = 0, padx = 10, pady = 10, sticky = E)

        # Window loop that keeps its open during the execution of the application
        chat_window.mainloop()


# Function that centralizes the window on the user's screen given the dimension of the window
def centralize(window, width, height):

    width_screen   = window.winfo_screenwidth()                 # Getting information about the
    height_screen  = window.winfo_screenheight()                # user's screen

    posx = width_screen/2 - width/2                             # Calculating position for centralize
    posy = height_screen/2 - height/2                           # the window

    window.geometry("%dx%d+%d+%d" %(width, height, posx, posy)) # Specifying geometry attributes of the window


def Login_Wind():
    # Window creation and assignment of its attributes
    login_window = Tk()                             # Creating window
    login_window['bg'] = color1                     # Background color
    login_window.title('Login')                     # Title
    login_window.iconbitmap('./icons/login_icon.ico')       # Icon
    centralize(login_window, 420, 60)               # Call of the function that centralizes
                                                    # the established 420x60 window
    login_window.resizable(False, False)            # Resizable property disable

    # Frame's creation
    frame_login = Frame(login_window, bg = color1)  # Creating frame and specifying its attributes

    Client.connect(Serv_addr)                       # Connecting to server out of main loop so
                                                    # the client address and port are not changed

    # Widgets

    # Creating Label, that specifies the username requirement, and its attributes
    label_us = Label(frame_login, font = fonte, bg = color1, fg = color2,
                     text = "Nome de Usuário:")

    # Creating Entry Text Box, for username value, and its attributes
    username  = Entry (frame_login, font = fonte, bg = color4, fg = color2)

    # Creating Login Submission Button and its attributes
    submitbtn = Button(frame_login, font = fonte, fg = color2, bg = color3,
                       text = 'Login', command = lambda: chat(login_window, username.get()))

    # Placing the Frame and its widgets at specify positions of the window for building the interface
    frame_login.grid (row = 0, column = 1, ipadx = 10, padx = 10, ipady = 10, pady = 10)
    label_us.grid    (row = 0, column = 0, ipadx = 10, padx = 1)
    username.grid    (row = 0, column = 1, ipadx = 1,  padx = 1)
    submitbtn.grid   (row = 0, column = 2, ipadx = 10, padx = 10)

    # Window loop that keeps its open during the execution of the application
    login_window.mainloop()


# Call of the main function
Login_Wind()