import socket
from charm.toolbox.integergroup import IntegerGroupQ, integer
from functools import reduce
import random
from time import sleep
import json

HOST = "0.0.0.0"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

G = IntegerGroupQ()

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect(ADDR)

def receive_params():
    while True:
        try:
            msg = c_socket.recv(BUFSIZ).decode("utf-8")
            params = json.loads(msg)
            G.setparam(params["p"], params["q"])
            G.r = 2
            g = integer(params["g"],G.p)
            print("Received Parameters")
            return g, params["id"], params["master"]
        except OSError:  # Possibly client has left the chat.
            break

def gen_proof(g, x):
    v = G.random()
    g_v = g ** v
    h = G.hash(g, g_v, (g ** x), id)
    r = (v - x * h)
    return (int(g_v), int(r))

def send_gx(g, id):
    x = G.random()
    g_x = g ** x
    # print(g_x)
    params = {
    "id": id,
    "g_x": int(g_x),
    "proof": gen_proof(g, x)
    }
    message = json.dumps(params).encode("utf-8")
    c_socket.send(message)
    return g_x, x

def receive_gxs():
    while True:
        try:
            msg = c_socket.recv(BUFSIZ).decode("utf-8")
            params = json.loads(msg)
            # print(params)
            # numbers = [number for number in msg.split()]
            # print(numbers)
            return params
            # return [integer(int(number), G.p) for number in numbers]
        except OSError:  # Possibly client has left the chat.
            break

def multiply(list):
    return reduce(lambda x, y: x * y, list, integer(1, G.p))


def compute_g_y(numbers, id):
    before = []
    after = []
    for element in numbers:
        if element["id"] < id:
            before.append(integer(element["g_x"], G.p))
        elif element["id"] > id:
            after.append(integer(element["g_x"], G.p))
    mult_before = multiply(before)
    mult_after = multiply(after)
    return mult_before / mult_after

def send_answer(g_y, x, id):
    r = G.random()
    while True:
        answer = input("Enter the answer: (0 or 1)\n")
        if answer == "1":
            g_c_y = g_y ** r
            break
        elif answer == "0":
            g_c_y = g_y ** x
            break
    sleep(random.random())
    params = {
    "gcy": int(g_c_y),
    "id": id,
    }
    message = json.dumps(params).encode("utf-8")
    c_socket.send(message)
    return g_c_y

def receive_gcy():
    while True:
        try:
            msg = c_socket.recv(BUFSIZ).decode("utf-8")
            params = json.loads(msg)
            # print(params)
            answers = []
            for element in params:
                answers.append(integer(element["gcy"], G.p))
            return answers
        except OSError:  # Possibly client has left the chat.
            break

def main():
    g, id, master = receive_params()
    if master:
        number = int(input("Enter the number of participants:\n"))
        question = input("Enter the question: \n")
        params = {
        "number": number,
        "question": question
        }
        # print(params)
        message = json.dumps(params).encode("utf-8")
        c_socket.send(message)
        sleep(0.1)
    g_x, x = send_gx(g, id)
    params = receive_gxs()
    question = params["question"]
    numbers = params["gxs"]
    g_y = compute_g_y(numbers, id)
    # print(g_y)
    print("Question:")
    print(question)
    g_c_y = send_answer(g_y, x, id)
    # print(g_c_y)
    print("Waiting for other answers...")
    answers = receive_gcy()
    a = reduce(lambda x, y: x * y, answers, integer(1, G.p)) % G.p
    if a == integer(1, G.p):
        print("Answer: No")
    else:
        print("Answer: Yes")


if __name__ == '__main__':
    main()
