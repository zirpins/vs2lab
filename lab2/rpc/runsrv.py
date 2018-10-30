import logging

import rpc
from context import lab_channel, lab_logging

lab_logging.setup()
logger = logging.getLogger('vs2lab.lab2.rpc.runsrv')

chan = lab_channel.Channel()
chan.channel.flushall()
logger.info('Flushed all redis keys.')

srv = rpc.Server()
srv.run()
