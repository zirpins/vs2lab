"""
Simple implementation of a chord client
- just the name system and name resolution parts, no data storage
- individual ChordClients might be run on any node for name resolution 
- client runs name resolution locally cycling over multiple nodes
"""

import logging
import random

import constChord


class ChordClient():
    """
    ChordClient implements a stepwise name resolution startegy.
    """

    def __init__(self, channel):
        self.channel = channel  # Create reference to communication channel
        # Register client process with channel
        self.node_id = int(self.channel.join('client'))
        self.logger = logging.getLogger("vs2lab.lab4.chordclient.ChordClient")

    def run(self):
        self.channel.bind(str(self.node_id))  # bind current pid

        # Lookup current nodes of the chord ring
        processes = [i.decode()
                     for i in list(self.channel.channel.smembers('node'))]

        # Get random lookup parameters
        node : int = int(processes[random.randint(0, len(processes) - 1)])
        key : int = random.randint(0, self.channel.MAXPROC - 1)

        self.logger.info(
            "Client node {:04n} sending LOOKUP request for {:04n} to ring node {:04n}"
                .format(self.node_id, key, node))

        # ... lookup code

        self.logger.info(
            "Client node {:04n} received final answer succ({:04n})={:04n} from {:04n}."
                .format(self.node_id, key, node, node))

        self.channel.send_to(processes, constChord.STOP)
