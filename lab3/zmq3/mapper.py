import sys
import pickle
import zmq

import constPipe

me = str(sys.argv[1])

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
push_socket = context.socket(zmq.PUSH)

address = ""

match me:
    case "1":
        address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT2
    case "2":
        address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT3
    case "3":
        address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT4

address5 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT5;
address6 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT6;

push_socket.bind(address)
push_socket.connect(address5)
push_socket.connect(address6)

pull_address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1

pull_socket.connect(pull_address)

while True:
    line: str = pull_socket.recv()
    print(f"got line {line}")
    for word in line.split():
        print(f"Sending {word}")
        push_socket.send(pickle.dumps((word, 1)))



