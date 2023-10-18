"""
Simple client server unit test
"""

import logging
import unittest

from context import lab_logging
from lab1.clientserver import Server, Client, UNKNOWN_ENTRY_REPLY
from lab1.phonebook_helper import get_phonebook

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The tests"""

    def test_srv_get(self):
        """Test simple search of known names"""
        names = list(get_phonebook().keys())
        with Server() as srv:
            with Client() as cl:
                for name in names:
                    self.assertNotEqual(UNKNOWN_ENTRY_REPLY, cl.get(name))

    def test_srv_get_error(self):
        """Test simple search of unknown names"""
        names = ["We", "Must", "Not", "Exist"]
        with Server() as srv:
            with Client() as cl:
                for name in names:
                    self.assertEqual(UNKNOWN_ENTRY_REPLY, cl.get(name))

    def test_srv_get_all(self):
        """Test simple search of ALL known names"""
        number_of_entries = 500
        with Server(entries=number_of_entries) as srv:
            with Client() as cl:
                # all lines except the last one are entries, separated by \n
                self.assertEqual((len(cl.get_all().split("\n")) - 1), number_of_entries)


if __name__ == "__main__":
    unittest.main()
