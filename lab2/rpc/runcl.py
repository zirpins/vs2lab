import time
import rpc
import logging

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()


def returnMessage(newList):  
    print("Answer from Server: {}".format(newList.value))
    cl.serverIsBusy = False

def ackPrint(ackMessage):
    print(ackMessage)


base_list = rpc.DBList({'Erster Eintrag'})
cl.append('Zweiter Eintrag', base_list, ackPrint, returnMessage) #functionsparameter

while(cl.serverIsBusy):
    print("Client is working on main thread...")
    time.sleep(1)

cl.stop()
