"""
Simple client server unit test
"""

import logging
import threading
import unittest
import re

import clientserverTelefon
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""
    _server = clientserverTelefon.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    patternGETALL = r'^GETALL:\s.*$'

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserverTelefon.Client()  # create new client for each test

    def test_srv_getEntry(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.get("Alice")
        self.assertEqual(msg, 'GET: Alice: 987-654-3210')

    def test_srv_getAll(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.getAll()
        self.assertNotEqual(re.match(TestEchoService.patternGETALL, msg), None)
    
    def test_srv_getEntryNotFound(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.get("ce")
        self.assertEqual(msg, 'Contact not found')

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
