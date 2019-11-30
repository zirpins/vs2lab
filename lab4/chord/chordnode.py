"""
Simple implementation of a chord DHT (distributed hash table)
- just the name system and name resolution parts, no data storage
- communication via lab_channel
- channel-based node management for simplification
- search local succ via finger table
- each chord node runs a ChordNode instance for maintaining the ring and local
  succ lookup
"""

import logging

import constChord


class ChordNode:
    """
    Implementation of a chord ring node
    """

    def __init__(self, channel):
        """
        :param channel: a communication chanel instance to be used
        """
        self.channel = channel  # Create reference to communication channel

        self.n_bits = channel.n_bits  # Number of bits for the ID space
        self.MAXPROC = channel.MAXPROC  # Maximum num of processes

        # Register node process with channel
        self.node_id = int(self.channel.join('node'))

        # Initialize Finger Table (FT):
        # - FT[0] will be predecessor
        self.finger_table = [-1 for _ in range(self.n_bits + 1)]

        self.node_list = []  # Nodes discovered so far

        self.logger = logging.getLogger("vs2lab.lab4.chordnode.ChordNode")

    def in_between(self, key, lower_bound, upper_bound) -> bool:
        """
        Check if key is located in the name range between two given nodes considering the ring topology
        :param key:
        :param lower_bound: first node name
        :param upper_bound: second node name
        :return:
        """
        if lower_bound <= upper_bound:
            return lower_bound <= key < upper_bound
        else:
            return (lower_bound <= key < upper_bound + self.MAXPROC) or (
                    lower_bound <= key + self.MAXPROC and key < upper_bound)

    def add_node(self, node_id) -> None:
        """
        Register new ring node name
        :param node_id: new name
        :return: None
        """
        self.node_list.append(int(node_id))  # append name to list
        self.node_list = list(set(self.node_list))  # get rid of duplicates
        self.node_list.sort()  # create ring order

    def delete_node(self, node_id) -> None:
        """
        Remove node name from local list
        :param node_id: name to purge
        :return: None
        """
        assert node_id in self.node_list, 'node_id unknown'
        del self.node_list[self.node_list.index(node_id)]
        self.node_list.sort()

    def finger(self, i) -> int:
        """
        Locate node to be registered for i'th row of finger table.
        The node is the first one after the i'th offset p+2^(i-1).
        The node is located in the set of known nodes.
        :param i: row of finger table
        :return: node for i'th row of finger table or None if unknown
        """
        succ = (self.node_id + pow(2, i - 1)) % self.MAXPROC  # initialize succ(p+2^(i-1)), start with address offset
        lwbi = self.node_list.index(self.node_id)  # initialize lower segment bound as own index in node set (p)
        upbi = (lwbi + 1) % len(self.node_list)  # initialize upper segment bound as index of next neighbor

        for _ in range(len(self.node_list)):  # go through all segments of known nodes
            if self.in_between(succ, self.node_list[lwbi] + 1, self.node_list[upbi] + 1):
                return self.node_list[upbi]  # found successor
            (lwbi, upbi) = (upbi, (upbi + 1) % len(self.node_list))  # go to next segment

    def recompute_finger_table(self) -> None:
        """
        Trigger re-computation of finger table from known nodes
        :return: None
        """
        self.finger_table[0] = self.node_list[self.node_list.index(self.node_id) - 1]  # Predecessor
        self.finger_table[1:] = [self.finger(i) for i in range(1, self.n_bits + 1)]  # Successors

    def local_successor_node(self, key) -> int:
        """
        Locate successor of a key in local finger table
        :param key: key to be located
        :return: located node name
        """
        if self.in_between(key, self.finger_table[0] + 1, self.node_id + 1):  # key in (FT[0],self]
            return self.node_id  # node is responsible
        elif self.in_between(key, self.node_id + 1, self.finger_table[1]):  # key in (self,FT[1]]
            return self.finger_table[1]  # successor responsible
        for i in range(1, self.n_bits):  # go through rest of FT
            if self.in_between(key, self.finger_table[i], self.finger_table[(i + 1) ]):
                return self.finger_table[i]  # key in [FT[i],FT[i+1])
        if self.in_between(key, self.finger_table[-1], self.finger_table[0] + 1): # key outside FT
            return self.finger_table[-1]  # key in [FT[-1],FT[0]]
        assert False # we cannot be here

    def enter(self):
        self.channel.bind(str(self.node_id))  # bind current pid
        self.add_node(self.node_id)

        # Initialize the node
        # Get all nodes from channel for bootstrapping
        nodes = {node.decode() for node in self.channel.channel.smembers('node')}
        others = list(nodes - {str(self.node_id)})
        for other_node in others:  # for all other ring nodes
            # register current ring locally (might change later)
            self.add_node(other_node)
            # make this node known to all others
            self.channel.send_to([other_node], constChord.JOIN)
        self.recompute_finger_table()  # initialize local finger table

        self.logger.info("ChordNode {:04n} ready.".format(self.node_id))

    def run(self):
        while True:  # Start node operation loop
            message = self.channel.receive_from_any()  # Wait for any request
            sender: str = message[0]  # Identify the sender
            request = message[1]  # And the actual request

            # If sender is a node (that stays in the ring) then update known nodes
            if request[0] != constChord.LEAVE and self.channel.channel.sismember('node', sender):
                self.add_node(sender)  # remember sender node

            if request[0] == constChord.STOP:  # this node is requested to shutdown
                self.logger.debug("Node {:04n} received STOP from {:04n}."
                                  .format(self.node_id, int(sender)))
                break

            if request[0] == constChord.LOOKUP_REQ:  # A lookup request
                self.logger.info("Node {:04n} received LOOKUP {:04n} from {:04n}."
                                 .format(self.node_id, int(request[1]), int(sender)))

                # look up and return local successor 
                next_id: int = self.local_successor_node(request[1])
                self.channel.send_to([sender], (constChord.LOOKUP_REP, next_id))

                # Finally do a sanity check
                if not self.channel.exists(next_id):  # probe for existence
                    self.delete_node(next_id)  # purge disappeared node

            elif request[0] == constChord.JOIN:
                # Join request (the node was already registered above)
                self.logger.debug("Node {:04n} received JOIN from {:04n}."
                                  .format(self.node_id, int(sender)))
                # we don't care for storage re-location in this example
                continue
            elif request[0] == constChord.LEAVE:  # Leave request
                self.logger.info("Node {:04n} received LEAVE from {:04n}."
                                 .format(self.node_id, int(sender)))
                self.delete_node(sender)  # update known nodes

            self.recompute_finger_table()  # adjust finger-table based on updated node set

        # print finger table status before termination
        print("FT[{:04n}]: {}"
              .format(self.node_id, ["{:04n}"
                      .format(finger_node) for finger_node in self.finger_table]))
