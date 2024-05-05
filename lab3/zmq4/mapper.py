# Task worker
# Connects PULL socket to tcp://localhost:5557
# Collects workloads from ventilator via that socket
# Connects PUSH socket to tcp://localhost:5558
# Sends results to sink via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq
import re


context = zmq.Context()
continueLoop = True

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender_even = context.socket(zmq.PUSH)
sender_even.connect("tcp://localhost:5558")

sender_odd = context.socket(zmq.PUSH)
sender_odd.connect("tcp://localhost:5559")

# Process tasks forever
while continueLoop:
    s = re.sub(r'[^\w\s]', '', receiver.recv().decode('utf-8')) 
    if(s=="__End__"):
        continueLoop = False

    listOfWords = s.strip().split()
    #print(listOfWords)


    for word in listOfWords:
        if(len(word)%2 == 0):
            #Send word to reducer 1
            print(word)
            sender_even.send_string(word.lower())
        else:
            #Send word to reducer2
            print(word)
            sender_odd.send_string(word.lower())

  