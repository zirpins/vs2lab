# Task sink
# Binds PULL socket to tcp://localhost:5558
# Collects results from workers via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq

reducer_id = str(sys.argv[1]) 
context = zmq.Context()

dictionary = {}
continueLoop = True

# Socket to receive messages on
receiver = context.socket(zmq.PULL)

#receiver.bind("tcp://*:5558")
if (reducer_id == "0"):
    print("Reducer 0")
    receiver.bind("tcp://localhost:5558")
else:
    print("Reducer 1")
    receiver.bind("tcp://localhost:5559")



# Process messages forever
while continueLoop:
    s = receiver.recv().decode('utf-8')
    if(s=="__end__" or s=="__end_"):
        continueLoop = False

    #print(s)

    if s in dictionary:
        # If the key exists, increment its value by 1
        dictionary[s] += 1
    else:
        # If the key does not exist, add the key with value 1
        dictionary[s] = 1
    
    print(f"Amount for {s} : ", dictionary[s])
    
with open("results.txt", 'a') as file:
        for key, value in dictionary.items():
            file.write(f"{key}: {value}\n")

print(dictionary)
