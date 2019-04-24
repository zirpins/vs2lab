import logging

import channel
from context import lab_channel, lab_logging

lab_logging.setup(stream_level=logging.DEBUG)
logger = logging.getLogger('vs2lab.lab2.channel.runsrv')

chan = lab_channel.Channel()
chan.channel.flushall()
logger.info('Flushed all redis keys.')

server = channel.Server()
server.run()
