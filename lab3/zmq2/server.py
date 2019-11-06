import time
import datetime
import zmq

import constPS

context = zmq.Context()
publisher = context.socket(zmq.PUB)  # create a publisher socket

address = "tcp://" + constPS.HOST + ":" + constPS.PORT  # how and where to communicate
publisher.bind(address)  # bind socket to the address

while True:
    time.sleep(5)  # wait every 5 seconds
    publisher.send(("TIME " + str(datetime.datetime.now().time())).encode())  # publish the current time
    publisher.send(("DATE " + str(datetime.date.today())).encode())  # publish the current date
