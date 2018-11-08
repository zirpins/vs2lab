import logging

import constRPYC
import rpyc

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)
logger = logging.getLogger("vs2lab.lab2.rpyc.Client")

conn = rpyc.connect(constRPYC.SERVER, constRPYC.PORT)  # Connect to the server
logger.info("Connected.")

# the exposed service lives in conn.root
dblist = conn.root

ret = dblist.append(2)  # Call an exposed operation,
logger.info("Append 2: '{}'".format(str(ret)))

ret = dblist.append(4)  # and append two elements
logger.info("Append 4: '{}'".format(str(ret)))

ret = dblist.value()  # Print the result
logger.info("Stored value: '{}'".format(str(ret)))
