import logging
from typing import List, Any

import constRPYC
import rpyc
from rpyc.utils.server import ThreadedServer

from context import lab_logging

lab_logging.setup()
logger = logging.getLogger("vs2lab.lab2.rpyc.server")


class DBList(rpyc.Service):
    value: List[Any] = [] # not visible from remote

    # visible functions start with 'exposed_'
    def exposed_append(self, data):
        self.value = self.value + [data]
        return self.value

    def exposed_value(self):
        return self.value


if __name__ == "__main__":
    server = ThreadedServer(DBList, port=constRPYC.PORT)
    logger.info("Server starting...")
    server.start()
