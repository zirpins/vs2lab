import threading
import time
import constRPC

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
        self.serverIsBusy = False

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list, clientAck, clientCallback):
    # Define a function to handle receiving response from server in a separate thread
        def waitForMessage():
            msgrcv = self.chan.receive_from(self.server) # Wait for list
            clientCallback(msgrcv[1])
    
    # Send request to server
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
    
    # Receive Server Ack
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        self.serverIsBusy = True
        clientAck(msgrcv)
    
    # Open new thread to wait for new list from server
        thread = threading.Thread(target=waitForMessage)
        thread.start()
    
    # Main thread returns while the new thread waits for server response
        return


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
                    self.chan.send_to({client}, "Received your message")
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    time.sleep(10)
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore
