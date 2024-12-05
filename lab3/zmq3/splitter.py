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

address1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT2
address2 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT3
address3 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT4

# push_socket.connect(address1)
# push_socket.connect(address2)
# push_socket.connect(address3)

time.sleep(2)

with open("text.txt") as f: file = f.readlines()

for line in file:
    push_socket.send_string(line)
