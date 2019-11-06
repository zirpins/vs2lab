import zmq

import constRR

context = zmq.Context()

address = "tcp://" + constRR.HOST + ":" + constRR.PORT2  # how and where to connect
requester = context.socket(zmq.REQ)  # create request socket

requester.connect(address)  # request connection and go on 

for i in range(3): # 3 times
    requester.send(b"Hello vs2lab")  # send message and go on
    print("Sent {}. request".format(i+1))  # print ack
    message = requester.recv()  # block until response
    print(message.decode() + " " + str(i+1) + " time")  # print result
