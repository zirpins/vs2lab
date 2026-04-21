import constRPC
import threading
import time

from context import lab_channel


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None
        self.running = True

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        self.running = False
        self.chan.leave('client')

    def _listen(self, callback):
        while self.running:
            msgrcv = self.chan.receive_from(self.server)  # wait for response
            if msgrcv is not None:
                payload = msgrcv[1]
                msg_type = payload[0]
                data = payload[1]
                callback(msg_type, data)  # pass it to caller


    def append(self, data, db_list, callback):
        assert isinstance(db_list, DBList)

        listener = threading.Thread(target=self._listen, args=(callback,))
        listener.start()  # start listening for response
        
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server

        for i in range(5):  # wait for response with timeout
            print(f"Client arbeitet weiter... {i}")
            time.sleep(1)


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    self.chan.send_to({client}, ("ACK", None)) # send ACK before processing

                    time.sleep(10)  # simulate long processing time
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, ("RESULT", result))  # return response
                else:
                    pass  # unsupported request, simply ignore
