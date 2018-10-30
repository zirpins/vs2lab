import logging

import rpyc

import constRPYC
from context import lab_logging

lab_logging.setup()


class Client:
    logger = logging.getLogger("vs2lab.b13_rpyc.Client")

    conn = rpyc.connect(constRPYC.SERVER, constRPYC.PORT)  # Connect to the server
    logger.info("Connected.")

    ret = conn.root.exposed_append(2)  # Call an exposed operation,
    logger.info("Append 2: '{}'".format(str(ret)))

    ret = conn.root.exposed_append(4)  # and append two elements
    logger.info("Append 4: '{}'".format(str(ret)))

    ret = conn.root.exposed_value()  # Print the result
    logger.info("Stored value: '{}'".format(str(ret)))
