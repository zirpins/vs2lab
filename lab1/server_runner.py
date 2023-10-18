import time

from lab1.clientserver import Server

"""Simple server example."""

s = Server(entries=500)
s.serve()
time.sleep(100)
s.stop()
