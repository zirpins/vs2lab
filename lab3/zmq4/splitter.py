# Task ventilator
# Binds PUSH socket to tcp://localhost:5557
# Sends batch of tasks to workers via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq
import random
import time


context = zmq.Context()

with open('results.txt', 'w'):  
    pass  

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

# Socket with direct access to the sink: used to synchronize start of batch
#sink = context.socket(zmq.PUSH)
#sink.connect("tcp://localhost:5558")

print("Press Enter when the workers are ready: ")
_ = input()
print("Sending tasks to workers...")

# The first message is "0" and signals start of batch
#sink.send(b'0')

with open('sentences.txt', 'r') as file:
    for line in file:
        sender.send_string(line)


# Give 0MQ time to deliver
time.sleep(2)