import pickle
import sys
import time

import zmq

import constPipe

address1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT2  # 1st task src
address2 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT3  # 2nd task src
address3 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT4  # 3rd task src

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

pull_socket.connect(address1)  # connect to task source 1
pull_socket.connect(address2)  # connect to task source 2
pull_socket.connect(address3)

time.sleep(1) 

wordcounts = {}

while True:
    work: {str, int} = pickle.loads(pull_socket.recv())  # receive work from a source
    if not work[0] in wordcounts:
        wordcounts[work[0]] = 1
    else:
        wordcounts[work[0]] = wordcounts[work[0]] + work[1]
    print(wordcounts)    
