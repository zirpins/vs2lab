import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

def callback(msg_type, result):
    if msg_type == "ACK":
        print("Server hat Request bestätigt (ACK)")
    elif msg_type == "RESULT":
        print("Finales Ergebnis:", result.value)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, callback)

for i in range(12):
    print("Main läuft unabhängig weiter...") # simulate main thread doing other work
    time.sleep(1)

cl.stop()
