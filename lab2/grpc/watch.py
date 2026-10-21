import logging

import grpc

import constGRPC
import dblist_pb2 as pb
import dblist_pb2_grpc as rpc
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)
logger = logging.getLogger("vs2lab.lab2.grpc.Watcher")

address = "{}:{}".format(constGRPC.SERVER, constGRPC.PORT)
with grpc.insecure_channel(address) as channel:
    stub = rpc.DBListStub(channel)
    logger.info("Watching {} for 30 s ...".format(address))
    try:
        # Server-Streaming: jedes Element kommt als eigene Nachricht
        for item in stub.Watch(pb.Empty(), timeout=30.0):
            logger.info("Item: '{}'".format(item.data))
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            logger.info("Deadline reached, stream closed.")
        else:
            raise
