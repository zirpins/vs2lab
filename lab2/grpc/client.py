import logging

import grpc

import constGRPC
import dblist_pb2 as pb  # von protoc generiert: Nachrichtentypen
import dblist_pb2_grpc as rpc  # von protoc generiert: Client-Stub
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)
logger = logging.getLogger("vs2lab.lab2.grpc.Client")

address = "{}:{}".format(constGRPC.SERVER, constGRPC.PORT)
with grpc.insecure_channel(address) as channel:  # Binding: Adresse + Port
    stub = rpc.DBListStub(channel)  # generierter Client-Stub
    logger.info("Connected to {}.".format(address))

    # synchroner (unärer) RPC mit Deadline von 1 s
    reply = stub.Append(pb.Item(data="2"), timeout=1.0)
    logger.info("Append 2: {}".format(list(reply.data)))

    # asynchroner RPC: Future sofort zurück, Ergebnis später abholen
    future = stub.Append.future(pb.Item(data="4"))
    logger.info("Append 4 sent, doing other work ...")
    logger.info("Append 4: {}".format(list(future.result().data)))

    # Typsicherheit: falscher Feldtyp fällt schon beim Erzeugen der Nachricht auf
    try:
        pb.Item(data=42)
    except TypeError as e:
        logger.info("Type check in client stub: Item.data expects str ({})".format(e))
