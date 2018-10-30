import logging
from typing import List, Any

import rpyc
from rpyc.utils.server import ForkingServer

import constRPYC
from context import lab_logging

lab_logging.setup()
logger = logging.getLogger("vs2lab.b13_rpyc.server")


class DBList(rpyc.Service):
    value: List[Any] = []

    def exposed_append(self, data):
        self.value = self.value + [data]
        return self.value

    def exposed_value(self):
        return self.value


if __name__ == "__main__":
    server = ForkingServer(DBList, port=constRPYC.PORT)
    logger.info("Server starting...")
    server.start()
