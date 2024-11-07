"""
Client and server using classes
"""

import logging
import socket
import json

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    tel_book = {'Florian': '13899985', 'Maximilian': '762843', 'Testmensch': '00000'}

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped

                    msg_in = data.decode('ascii')
                    self._logger.info(f"Received message {msg_in}")
                    result: str

                    if msg_in.startswith("GETALL"):
                        result = json.dumps(self.tel_book)
                        self._logger.info(f"Received GETALL request")

                    elif msg_in.startswith("GET"):
                        query = msg_in.split("&")[1]
                        self._logger.info(f"Received GET request with query {query}")
                        if not query in self.tel_book:
                            result = f"No entry found for query {query}"
                            self._logger.info(result)
                        else:
                            result = self.tel_book[query]
                            self._logger.info(f"Found entry {result}")

                    else:
                        result = "Bad Operation"

                    connection.send(result.encode('ascii'))  # return sent data plus an "*"
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        return msg_out
    
    def get(self, query: str):
        self.logger.info(f"Sending GET query for: {query}")
        return self.call("GET&" + query)

    def get_all(self):
        self.logger.info("Sending GETALL request")
        return self.call("GETALL")

    def close(self):
        """ Close socket """
        self.sock.close()
        self.logger.info("Socket closed")
