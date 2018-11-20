import zmq

import constPS

context = zmq.Context()
subscriber = context.socket(zmq.SUB)  # create a subscriber socket

address = "tcp://" + constPS.HOST + ":" + constPS.PORT  # how and where to communicate
subscriber.connect(address)  # connect to the server

subscriber.setsockopt(zmq.SUBSCRIBE, b"TIME")  # subscribe to TIME messages

for i in range(5):  # Five iterations
    time = subscriber.recv()  # receive a message
    print(time)
