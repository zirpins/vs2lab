import channel
from context import lab_logging

lab_logging.setup()

client = channel.Client()
client.run()
