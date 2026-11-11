import pickle
import sys
import time

import zmq

import constPipe

me = str(sys.argv[1])
address1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  # 1st task src
address2 = "tcp://" + constPipe.SRC2 + ":" + constPipe.PORT2  # 2nd task src

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket

pull_socket.connect(address1)  # connect to task source 1
pull_socket.connect(address2)  # connect to task source 2

print("{} started".format(me))

while True:
    src_id, workload = pickle.loads(pull_socket.recv())  # receive work from a source (pickle: trusted peers only)
    print("{} received workload {} from {}".format(me, workload, src_id))
    time.sleep(workload * 0.01)  # pretend to work
