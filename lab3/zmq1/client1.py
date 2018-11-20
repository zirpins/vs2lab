import zmq

import constRR

context = zmq.Context()

address = "tcp://" + constRR.HOST + ":" + constRR.PORT1  # how and where to connect
requester = context.socket(zmq.REQ)  # create request socket

requester.connect(address)  # request connection and go on 
requester.send(b"Hello vs2lab")  # send message and go on
print("Sent request")  # print ack
    
message = requester.recv()  # block until response
print(message.decode())  # print result

requester.send(b"STOP")  # tell server to stop
