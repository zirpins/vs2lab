import time
import rpc
import logging

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()


# Callback Function to print returned list from server
def returnMessage(newList):  
    print("Answer from Server: {}".format(newList.value))
    cl.serverIsBusy = False

# Function to print Ack message from server
def ackPrint(ackMessage):
    print("Answer from Server: " + ackMessage[1] + " from Server " +  ackMessage[0])

base_list = rpc.DBList({'Old Entry'})
cl.append('Newly appended Entry', base_list, ackPrint, returnMessage) 

# Doing work while the other thread is waiting for server response with list
while(cl.serverIsBusy):
    print("Client is working on main thread...")
    time.sleep(1)

cl.stop()
