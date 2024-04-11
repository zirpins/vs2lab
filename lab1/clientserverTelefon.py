"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging
import re

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    patternGET = r'^GET\s.*$'  # Pattern to match GET ...
    patternGETALL = r'^GETALL'  # Pattern to match GETALL

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
        self.contacts = {
            'John': '123-456-7890',
            'Alice': '987-654-3210',
            'Bob': '555-555-5555',
            'Eve': '111-222-3333',
            'Charlie': '444-444-4444',
            'Diana': '777-777-7777',
            'Frank': '888-888-8888',
            'Grace': '999-999-9999',
            'Harry': '666-666-6666',
            'Irene': '333-333-3333'
        }
        self._logger.info("Contacts dictionary initialized")

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

                    # Handle the request
                    response = self.handle_request(data.decode('ascii'))
                    
                    # Send response back to the client
                    connection.send(response.encode('ascii'))  # return sent data plus an "*"

                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def handle_request(self, request):
        """Handle different requests"""
        if re.match(Server.patternGETALL, request):
            self._logger.info("Recieved GETALL request")
            contact_info = ', '.join([f'{name}: {number}' for name, number in self.contacts.items()])
            return f"GETALL: {contact_info}"
        elif re.match(Server.patternGET, request):
            self._logger.info("Recieved GET request")
            trimmed_data = request.strip()
            name = trimmed_data.split()[-1].strip()

            if name in self.contacts:
                return f"GET: {name}: {self.contacts[name]}"
            else:
                return "Contact not found"
        else:
            self._logger.info("Unexpected request format")
            return "Unexpected error occured"

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

    def get(self, msg_in=""):
        return self.call(f"GET {msg_in}")
    
    def getAll(self):
        return self.call("GETALL")

    def close(self):
        """ Close socket """
        self.sock.close()
