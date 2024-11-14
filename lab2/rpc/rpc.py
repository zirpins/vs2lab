import constRPC

from context import lab_channel
import threading
import time

class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:

    class Receiver(threading.Thread):
        def __init__(self, chan, server, callback):
            threading.Thread.__init__(self)
            self.chan = chan
            self.server = server
            self.callback = callback

        def run(self):
            msgrcv = self.chan.receive_from(self.server)  # wait for response
            self.callback(msgrcv[1]) # pass it to caller


    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list, callback):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        ack = self.chan.receive_from(self.server)
        if ack[1] == 'ACK':
            receiver = self.Receiver(self.chan, self.server, callback)
            receiver.start()



   

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
                    self.chan.send_to({client}, 'ACK')
                    time.sleep(10)
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore
    
    # def callback(self, val, client):
    #     self.chan.send_to({client}, val)


# class AppendAsync(threading.Thread):
#     def __init__(self, data, dblist, callback, client):
#         threading.Thread.__init__(self)
#         self.data = data
#         self.dblist = dblist
#         self.callback = callback
#         self.client = client

#     def run(self):
        
#         assert isinstance(self.dblist, DBList)
#         self.callback(self.dblist.append(self.data), self.client)
