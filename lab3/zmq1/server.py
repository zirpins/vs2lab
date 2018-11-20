import zmq

import constRR

address1 = "tcp://" + constRR.HOST + ":" + constRR.PORT1  # how and where to connect
address2 = "tcp://" + constRR.HOST + ":" + constRR.PORT2  # how and where to connect

context = zmq.Context()
reply_socket = context.socket(zmq.REP)  # create reply socket
 
reply_socket.bind(address1)  # bind socket to address
reply_socket.bind(address2)  # bind socket to address

while True:
    message = reply_socket.recv()  # wait for incoming message
    if b"STOP" not in message:  # if not to stop...
        print("Received " + message.decode())
        reply_socket.send((message.decode() + "*").encode())  # append "*" to message
    else:  # else...
        break  # break out of loop and end
