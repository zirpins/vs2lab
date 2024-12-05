import sys
import pickle
import time

import zmq

import constPipe

me = str(sys.argv[1])

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  # how and where to connect
push_socket.bind(address)  # bind socket to address

time.sleep(2)

with open("text.txt") as f: file = f.readlines()

for line in file:
    push_socket.send_string(line)
