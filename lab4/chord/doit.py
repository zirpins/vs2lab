""" 
Chord Application
- defines a DummyChordClient implementation
- sets up a ring of chord_node instances
- Starts up a DummyChordClient
- nodes and client run in separate processes
- multiprocessing should work on unix and windows
"""

import time
import logging
import sys
from multiprocessing import Process

import chordnode as chord_node
import constChord

from context import lab_channel, lab_logging

lab_logging.setup(stream_level=logging.INFO)

if __name__ == "__main__":  # if script is started from command line
    m = 6  # Number of bits for linear names
    n = 16  # Number of nodes in the chord ring

    # Check for command line parameters m, n.
    if len(sys.argv) > 2:
        m = int(sys.argv[1])
        n = int(sys.argv[2])

    # Create a communication channel.,.  ö,
    chan = lab_channel.Channel(n_bits=m)
    chan.channel.flushall()


    class DummyChordClient:
        """A dummy client template with the channel boilerplate code"""
        def __init__(self, channel):
            self.channel = channel
            self.node_id = channel.join('client')

        def run(self):
            self.channel.bind(self.node_id)
            print("Implement me pls...")
            chan.send_to(  # a final multicast
                [i.decode()
                     for i in list(self.channel.channel.smembers('node'))],                
                constChord.STOP)

    # Init n chord nodes and a clint
    nodes = [chord_node.ChordNode(chan) for i in range(n)]
    client = DummyChordClient(chan)

    # start n chord nodes in separate processes
    children = []
    for i in range(n):
        nodeproc = Process(
            target=lambda n: n.run(),
            name="ChordNode-"+str(i),
            args=(nodes[i],))
        children.append(nodeproc)
        nodeproc.start()
        time.sleep(0.25)

    clientproc = Process(
        target=lambda c: c.run(),
        name="ChordClient",
        args=(client,))

    # start client and wait for it to finish
    clientproc.start()
    clientproc.join()

    # wait for nodes to finish
    for nodeproc in children:
        nodeproc.join()
