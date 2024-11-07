"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    def test_srv_get(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.get("Florian")
        self.assertEqual(msg, '13899985')

    def test_srv_get2(self):
        msg = self.client.get("Maximilian")
        self.assertEqual(msg, '762843')

    def test_srv_getall(self):
        msg = self.client.get_all()
        self.assertEqual(msg, '{"Florian": "13899985", "Maximilian": "762843", "Testmensch": "00000"}')

    def test_not_found(self):
        msg = self.client.get("Jurgen")
        self.assertEqual(msg, "No entry found for query Jurgen")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
