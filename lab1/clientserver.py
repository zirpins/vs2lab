"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True
    _phonebook = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])

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
                    temp = data.decode('ascii').strip().split() 
                    
                    command = temp[0]

                    if len(temp) == 2:
                        params = temp[1]

                    if command == "GET":
                        result = self.get(params)
                        connection.send(result.encode('ascii'))
                    elif command == "GETALL":
                        result = self.get_all()
                        connection.send(result.encode('ascii'))
                    else:
                        connection.send(data + "*".encode('ascii'))  # return sent data plus an "*"
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def get(self, name):
        number = self._phonebook.get(name)
        if number is not None:
            return str(number)
        else:
            return "Entry not found"

    def get_all(self):
        return ', '.join([f"{name}: {number}" for name, number in self._phonebook.items()])


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def get(self, name):

        """ Get entry from server """
        command = "GET " + name 
        self.sock.send(command.encode('ascii'))  # send command to server
        data = self.sock.recv(1024)  # receive the response
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return data.decode('ascii')  # return the result

    def get_all(self):
        """ Get all entries from server """
        command = "GETALL"
        self.sock.send(command.encode('ascii'))  # send command to server
        data = self.sock.recv(1024)  # receive the response
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return data.decode('ascii')  # return the result

    def close(self):
        """ Close socket """
        self.sock.close()
