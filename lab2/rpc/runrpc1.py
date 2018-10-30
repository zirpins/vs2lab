import os
import rpc1
from context import lab_channel, lab_logging
import logging

lab_logging.setup()
logger = logging.getLogger('vs2lab.b11_rpc1.runrpc1')

chan = lab_channel.Channel()
chan.channel.flushall()
logger.info('Flushed all redis keys.')

srv = rpc1.Server()
cl = rpc1.Client()

pid = os.fork()
if pid == 0:
    srv.run()
    os._exit(0)

cl.run()
base_list = rpc1.DBList({'foo'})
result_list = cl.append('bar', base_list)

print("Result: {}".format(result_list.value))

os._exit(0)
