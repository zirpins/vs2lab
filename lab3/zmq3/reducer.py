import pickle
import sys
import time

import zmq

import constPipe

me = str(sys.argv[1])

self_add = ""

match me:
    case "1":
        self_add = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT5
    case "2":
        self_add = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT6

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket
pull_socket.bind(self_add)

time.sleep(1) 

wordcounts = {}

while True:
    work: {str, int} = pickle.loads(pull_socket.recv())  # receive work from a source
    if not work[0] in wordcounts:
        wordcounts[work[0]] = 1
    else:
        wordcounts[work[0]] = wordcounts[work[0]] + work[1]
    print(wordcounts)    
