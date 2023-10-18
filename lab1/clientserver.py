"""
Client and server using classes
"""
import json
import logging
import socket
import threading

import const_cs
from context import lab_logging
from lab1.phonebook_helper import get_phonebook, generate_random_phonebook_entries

CMD_GET = "GET"
CMD_GETALL = "GETALL"

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long


class Server:
    """The server"""

    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")

    def __init__(self, big: bool = False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
        self._addressbook = get_phonebook()
        if big:
            self._addressbook.update(generate_random_phonebook_entries(500))
        self._serving = False
        self._serving_thread = None

    def __enter__(self):
        self.serve()

    def __exit__(self, type, value, traceback):
        self.stop()

    def serve(self):
        self._serving = True
        self._serving_thread = threading.Thread(target=self._serve_loop)
        self._serving_thread.start()
        self._logger.info("Server up.")

    def stop(self):
        self._serving = False
        self._serving_thread.join()

    def _serve_loop(self):
        """Serve forever"""
        self.sock.listen(1)
        while (
            self._serving
        ):  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (
                    connection,
                    address,
                ) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    # parse data
                    ret_val = self._parse_data(data)
                    connection.send(ret_val.encode("utf-8"))
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def _parse_data(self, data) -> str:
        """Parse data"""
        # decode bytes to str
        empty_msg = ""
        msg_in = data.decode("utf-8")
        self._logger.info("Server received: " + msg_in)

        # parse json
        try:
            msg_json = json.loads(msg_in)
        except json.decoder.JSONDecodeError:
            self._logger.error("Server received invalid json: " + msg_in)
            return empty_msg

        # check if json contains command
        if CMD_GET in msg_json:
            return self._get(msg_json[CMD_GET])
        elif CMD_GETALL in msg_json:
            return self._getall()
        else:
            self._logger.error("Server received invalid json: " + msg_in)
            return empty_msg

    def _get(self, name: str) -> str:
        if name in self._addressbook:
            self._logger.info("Server found " + name + " in addressbook.")
            return self._addressbook[name]
        else:
            self._logger.info("Server did not find " + name + " in addressbook.")
            return "Name not in addressbook."

    def _getall(self) -> str:
        out = ""
        for name in self._addressbook:
            out += name + ": " + self._addressbook[name] + "\n"
        return out


class Client:
    """The client"""

    def __init__(self):
        self.logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _call(self, msg_in: str) -> str:
        """Call server"""
        self.logger.info(f"Send {msg_in}")
        self.sock.send(msg_in.encode("utf-8"))
        # Receive data in chunks until there is no more data
        received_data = b""
        try:
            self.sock.settimeout(0.01)
            while True:
                chunk = self.sock.recv(1024)  # receive a chunk of data
                if not chunk:
                    break  # no more data to receive, break the loop
                received_data += chunk
        except socket.timeout:
            pass
        msg_out = received_data.decode("utf-8")
        return msg_out

    def get(self, name: str) -> str:
        """Get phone-number for name"""
        msg = json.dumps({CMD_GET: name})
        return self._call(msg)

    def get_all(self) -> str:
        """Get all names and phone-numbers"""
        msg = json.dumps({CMD_GETALL: ""})
        return self._call(msg)

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def close(self):
        """Close socket"""
        self.sock.close()
