import rpc
import logging
import time

from context import lab_logging

def callback_receiver(msg):
    print("Result: {}".format(msg.value))

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, callback_receiver)

x = 1
while x < 15:
    print(x)
    x = x + 1
    time.sleep(1)
    
# print("Result: {}".format(result_list.value))

cl.stop()

