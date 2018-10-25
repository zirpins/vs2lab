import os
import unittest

import clientserver

class TestEchoService(unittest.TestCase):
    def setUp(self):
        super().setUp()
        server = clientserver.Server()
        pid = os.fork()
        if pid == 0:
            server.serve()
            os._exit(0)
        self.client = clientserver.Client()

    def test_srv_get(self):
        msg = self.client.call("Hello VS2Lab")
        self.assertEqual(msg, 'Hello VS2Lab*')


if __name__ == '__main__':
    unittest.main()
