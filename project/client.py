#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from charm.toolbox.integergroup import IntegerGroupQ, integer


def receive():
    """Handles receiving of messages."""
    paramstage = True
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            if(paramstage):
                numbers = [int(number) for number in msg.split()]
                print(*numbers[:2])
                G.setparam(*numbers[:2])
                g = integer(numbers[2],G.p)
                print("gen:", g)
                G.r = 2
                x = G.random()
                print("x", x)
                send_gx(g,x)
                paramstage = False
            print(msg.decode("utf8"))
        except OSError:  # Possibly client has left the chat.
            break

def send_gx(g, x):
    g_x = g**x
    print(g_x)
    client_socket.send(bytes(str(integer(g_x)), "utf8"))

def send():  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()



#----Now comes the sockets part----
HOST = "0.0.0.0"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
G = IntegerGroupQ()
g = None

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
