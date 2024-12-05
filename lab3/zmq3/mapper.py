import sys
import pickle
import zmq

import constPipe

me = str(sys.argv[1])

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
push_socket1 = context.socket(zmq.PUSH)
push_socket2 = context.socket(zmq.PUSH)

address5 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT5;
address6 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT6;

push_socket1.connect(address5)
push_socket2.connect(address6)

pull_address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1

pull_socket.connect(pull_address)

while True:
    line: str = pull_socket.recv()
    print(f"got line {line}")
    for word in line.split():
        print(f"Sending {word}")
        if len(word) % 2 == 0:
            push_socket1.send(pickle.dumps((word, 1)))
        else:
            push_socket2.send(pickle.dumps((word, 1)))



