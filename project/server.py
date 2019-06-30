#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from time import sleep
from charm.toolbox.integergroup import IntegerGroupQ, integer
import json

first_phase = True
broadcasted = False
number_of_part = 9999
question = ""

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    number = 1
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        params = {
        "p": int(GROUP.p),
        "q": int(GROUP.q),
        "g": int(GEN),
        "id": number,
        "master": number == 1
        }
        message = json.dumps(params).encode('utf-8')
        # client.send(bytes((str(GROUP.p) + " " + str(GROUP.q) + " " + str(integer(GEN))), "utf8"))
        client.send(message)
        addresses[client] = client_address
        sleep(0.1)
        Thread(target=handle_client, args=(client,number, number == 1)).start()
        number += 1


def handle_client(client, id, master):  # Takes client socket as argument.
    """Handles a single client connection."""
    global number_of_part
    global question
    clients[client] = id
    sleep(0.5)
    if master:
        msg = client.recv(BUFSIZ)
        params = json.loads(msg.decode("utf-8"))
        print(params)
        number_of_part = params["number"]
        question = params["question"]
    msg = client.recv(BUFSIZ)
    check_list(msg)
    while True:
        if len(gxs) == number_of_part:
            print(gxs)
            params = {
                "question": question,
                "gxs": gxs
            }
            test = json.dumps(params)
            client.send(test.encode("utf-8"))
            break
    msg = client.recv(BUFSIZ)
    params = json.loads(msg.decode("utf-8"))
    print(params)
    gcy_phase(msg)
    while True:
        if len(gcy) == number_of_part:
            print(gcy)
            test = json.dumps(gcy)
            client.send(test.encode("utf-8"))
            break
        # sleep(0.5)

def check_list(number):
    data = number.decode("utf-8")
    gxs.append(json.loads(data))


def gcy_phase(number):
    data = number.decode("utf-8")
    gcy.append(json.loads(data))

def broadcast(msg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(msg.encode("utf-8"))



clients = {}
addresses = {}
gxs = []
gcy = []


HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
GROUP = IntegerGroupQ()
GROUP.paramgen(16)
GEN = GROUP.randomG()

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
