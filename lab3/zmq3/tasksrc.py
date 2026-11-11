import pickle
import random
import sys
import time

import zmq

import constPipe

me = str(sys.argv[1])

host = constPipe.SRC1 if me == '1' else constPipe.SRC2  # check task src host
port = constPipe.PORT1 if me == '1' else constPipe.PORT2  # check task src port

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + host + ":" + port  # how and where to bind
push_socket.bind(address)  # bind socket to address

time.sleep(1)  # give all workers time to connect (needed for an even distribution)

for i in range(100):  # generate 100 workloads
    workload = random.randint(1, 100)  # compute workload
    push_socket.send(pickle.dumps((me, workload)))  # send workload to worker (pickle: trusted peers only)
