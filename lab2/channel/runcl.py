import channel
import logging

from context import lab_logging

lab_logging.setup(stream_level=logging.DEBUG)

client = channel.Client()
client.run()
