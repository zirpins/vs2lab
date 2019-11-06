import zmq
import time

import constRR

context = zmq.Context()

address = "tcp://" + constRR.HOST + ":" + constRR.PORT1  # how and where to connect
requester = context.socket(zmq.REQ)  # create request socket

requester.connect(address)  # request connection and go on 

for i in range(3): # 3 times
    requester.send(b"Hello world")  # send message and go on
    print("Sent {}. request".format(i+1))  # print ack
    message = requester.recv()  # block until response
    print(message.decode() + " " + str(i+1) + " time")  # print result

time.sleep(1) 
requester.send(b"STOP")  # tell server to stop
