import logging
import threading
from concurrent import futures

import grpc

import constGRPC
import dblist_pb2 as pb
import dblist_pb2_grpc as rpc
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)
logger = logging.getLogger("vs2lab.lab2.grpc.server")


class DBList(rpc.DBListServicer):
    """Implementierung der in dblist.proto definierten Schnittstelle"""

    def __init__(self):
        self.value = []
        self.changed = threading.Condition()  # weckt laufende Watch-Streams

    def Append(self, request, context):
        with self.changed:
            self.value.append(request.data)
            self.changed.notify_all()
            logger.info("Append '{}' -> {}".format(request.data, self.value))
            return pb.ItemList(data=self.value)

    def Watch(self, request, context):
        sent = 0
        while context.is_active():  # bis der Client abbricht oder die Deadline abläuft
            with self.changed:
                while sent == len(self.value) and context.is_active():
                    self.changed.wait(timeout=1.0)
                new = self.value[sent:]
            for data in new:
                yield pb.Item(data=data)
                sent += 1


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DBListServicer_to_server(DBList(), server)
    server.add_insecure_port("[::]:{}".format(constGRPC.PORT))
    server.start()
    logger.info("Server listening on port {}".format(constGRPC.PORT))
    server.wait_for_termination()
