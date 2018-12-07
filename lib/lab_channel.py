import logging
import os
import pickle
import random

import redis


class Channel:
    """
    Channel implements a communication channel for persistent asynchronous message exchange between member processes.
    Member processes (short: members) have to explicitly join a common global channel and obtain an identifier.
    Processes are associated with "subgroups" that can be queried to obtain a set of all members (e.g. all "servers").

    Members can use the channel to send/receive a message to/from a set of members or all other members.
    Messages might be any serializable object.

    Internally, the channel manages a set of queues.
    A queue is associates with two channel members: a sender and a receiver.
    It holds all messages from the sender to the receiver.
    Send operations of a caller push messages to respective caller-receiver queues for a set of receivers.
    Receive operations of a caller pop messages from respective sender-caller queues for a set of senders.

    Queues are implemented as redis lists.
    The key is a string representation of a list containing sender and receiver ids.
    That is, sender and receiver can always be identified by parsing the queue keys.

    Redis data Structures:

    Global Member Set
        Key: "members"
        Value: redis set of member ID strings
    Subgroup Member Sets
        Key: <subgroup>
        Value: redis set of member ID strings
    Global Queue List (containing all possible queue keys)
        Key: "xchan"
        Value: redis list of queue identifier objects
    Queues
        Key: "['<member1>','<member2>']"
        Value: redis list of message objects send fom member1 to member2
    """

    def __init__(self, n_bits: int = 5, host_ip: str = 'localhost', port_no: int = 6379):
        # create redis client
        self.channel = redis.StrictRedis(host=host_ip, port=port_no, db=0)
        # create dict of local pid bindings
        self.os_members = {}
        # Number of bits for pid addresses
        self.n_bits: int = n_bits
        # Maximum corresponding pid
        self.MAXPROC: int = pow(2, n_bits)
        # create instance logger
        self.logger = logging.getLogger('vs2lab.channel.Channel')
        self.logger.debug('New Channel created.')

    @staticmethod
    def __decode_set(raw) -> set:
        return {i.decode() for i in raw}

    def join(self, subgroup: str) -> str:
        """
        Join a process as a member to the global channel and associate it with a (sub)group. 
        Only members can communicate over the channel. 
        Subgroups can be used to retrieve a specific set of processes later (e.g. all servers).
        :param subgroup: an identifier for the grouping
        :return: global member id of the process.
        """
        # For concurrently assigning unique member ids, we need to use a transaction
        # atomically reading and writing the member set. This can be implemented by
        # means of the pipeline construct.
        with self.channel.pipeline() as pipe:
            while 1:
                try:
                    # Put a WATCH on the key that holds the member set
                    pipe.watch('members')
                    # After WATCHing, the pipeline is put into immediate execution
                    # mode until we tell it to start buffering commands again.
                    # This allows us to get the current value of the global member set
                    raw_members = pipe.smembers('members')
                    members = self.__decode_set(raw_members)
                    # Now construct new/unused random member id
                    remaining_ids = list(set([str(i) for i in range(self.MAXPROC)]) - members)
                    new_pid = random.choice(remaining_ids)
                    # Then we can put the pipeline back into buffered mode with MULTI
                    pipe.multi()
                    # Add new member id to global member set and subgroup
                    pipe.sadd('members', new_pid)
                    pipe.sadd(subgroup, new_pid)
                    # and finally, execute the pipeline (the set command)
                    pipe.execute()
                    # if a WatchError wasn't raised during execution,
                    # everything we just did happened atomically.
                    break
                except redis.WatchError:
                    # another client must have changed 'members' between
                    # the time we started WATCHing it and the pipeline's execution.
                    # our best bet is to just retry.
                    continue
        self.logger.info("Member {} joining {}.".format(new_pid, subgroup))

        # construct bidirectional queue names for new member and all existing members (if any)
        if len(members) > 0:
            xchan: list = [[new_pid, other] for other in members] + [[other, new_pid] for other in members]
            # push queue names to global list of all possible transfer queues
            for xc in xchan:
                self.channel.rpush('xchan', pickle.dumps(xc))
        return new_pid

    def leave(self, subgroup: str):
        """
        Unregister a process from the global channel (and subgroup).
        :param subgroup: subgroup identifier
        :return: None
        """
        # retrieve member id via os pid and validate it
        os_pid: int = os.getpid()
        pid: str = self.os_members[os_pid]
        assert self.channel.sismember('members', pid), 'member unknown'
        self.logger.info("Member {} leaving {}".format(pid, subgroup))

        # remove binding and global member element
        del self.os_members[os_pid]
        self.channel.srem('members', pid)

        # decode member set binary elements to string list
        raw_members: set = self.channel.smembers('members')
        members: set = self.__decode_set(raw_members)

        # construct bidirectional queue names for new member and all existing members (if any)
        if len(members) > 0:
            xchan: list = [[pid, other] for other in members] + [[other, pid] for other in members]
            # pop queue names from global list of all possible transfer queues
            for xc in xchan:
                self.channel.lrem('xchan', 0, pickle.dumps(xc))

        # remove member id from subgroup set
        self.channel.srem(subgroup, pid)

    def exists(self, pid: str) -> bool:
        """
        Check if pid is in global member set
        :param pid: process identifier
        :return: boolean value, true if pid is a member
        """
        return self.channel.sismember('members', pid)

    def bind(self, pid: str) -> int:
        """
        Associate os pid with channel member id.
        Thus a caller does not need to provide its id for every subsequent call.
        :param pid: identifier of process member
        :return: os pid value
        """
        # retrieve os pid and map to given member id
        os_pid: int = os.getpid()
        self.os_members[os_pid] = pid
        self.logger.debug("Member {} bound {}".format(pid, os_pid))
        return os_pid

    def subgroup(self, subgroup: str) -> set:
        """
        Retrieve members of a subgroup.
        :param subgroup: subgroup string identifier
        :return: set of member process identifiers
        """
        return self.__decode_set(self.channel.smembers(subgroup))

    @staticmethod
    def __queue_key(sender: str, receiver: str) -> str:
        """
        Construct queue name from sender and receiver ids.
        :param sender: member identifier
        :param receiver: member identifier
        :return: redis key
        """
        return str([sender, receiver])

    def send_to(self, destination_set: set, message: object) -> None:
        """
        Sends an asynchronous, persistent multicast message.
        :param destination_set: a set of member identifiers
        :param message: the message object to be send (see 'message format' in class doc)
        :return: None
        """
        # destination_set needs to contain string identifiers
        assert (type(k) is str for k in destination_set), 'type error'

        # lookup member id by pid and validate it
        caller: str = self.os_members[os.getpid()]
        assert self.channel.sismember('members', caller), 'unknown sender'
        self.logger.debug("{} sends {} to {}".format(caller, message, destination_set))

        # push message to incoming queues of all destinations
        for destination in destination_set:
            assert self.channel.sismember('members', destination), 'unknown receiver'
            self.channel.rpush(self.__queue_key(caller, destination), pickle.dumps(message))

    def send_to_all(self, message: object) -> None:
        """
        Sends an asynchronous, persistent broadcast message.
        The message is delivered to all queues of currently registered members.
        :param message: the message object to be send
        :return: None
        """
        # lookup member id by pid and validate it
        caller: str = self.os_members[os.getpid()]
        assert self.channel.sismember('members', caller), 'unknown sender'
        self.logger.debug("{} sends {} to all members".format(caller, message))

        members = self.__decode_set(self.channel.smembers('members'))
        # push message to incoming queues of all members
        for destination in members:
            self.channel.rpush([self.__queue_key(caller, destination)], pickle.dumps(message))

    def receive_from_any(self, timeout: int = 0) -> tuple:
        """
        Make a blocking request to take the next message off any of the callers' incoming queues.
        :param timeout: optional timeout for blocking read.
        :return: list containing the queue name and message
        """
        # lookup member id by pid and validate it
        caller = self.os_members[os.getpid()]
        assert self.channel.sismember('members', str(caller)), 'unknown receiver'

        # decode member set binary elements
        members: set = self.__decode_set(self.channel.smembers('members'))
        # construct incoming message queues for all members
        in_queues: set = {self.__queue_key(member, caller) for member in members}
        self.logger.debug("{} receives from {}".format(caller, in_queues))

        # block until new msg appears on one of the incoming queues
        result = self.channel.blpop(in_queues, timeout)
        if result is not None:
            # extract sender id from key part
            key: str = result[0].decode()
            sender: str = key.split("'")[1]
            # deserialize msg content
            message = pickle.loads(result[1])
            # log and return results
            self.logger.debug("{} received {} from {}".format(caller, message, sender))
            return sender, message

    def receive_from(self, sender_set: set, timeout: int = 0) -> tuple:
        """
        Make a blocking call to pop the next message off any of the callers' queues
        from the members specified in the sender_set attribute.
        :param sender_set: set of ids to watch respective incoming queues for a new message
        :param timeout: optional timeout for blocking call
        :return:
        """
        assert (type(k) is str for k in sender_set), 'Address type mismatch.'

        # lookup member id by pid and validate it
        caller: str = self.os_members[os.getpid()]
        assert self.channel.sismember('members', caller), 'unknown receiver'
        self.logger.debug("{} receives from {}".format(caller, sender_set))

        # validate all senders and construct incoming queues for them
        in_queues: set = set()
        for sender in sender_set:
            assert self.channel.sismember('members', sender), 'unknown sender'
            in_queues.add(self.__queue_key(sender, caller))

        # block until new msg appears on one of the queues
        result = self.channel.blpop(in_queues, timeout)
        if result is not None:
            # extract sender id from key part
            key: str = result[0].decode()
            sender: str = key.split("'")[1]
            # deserialize msg content
            message = pickle.loads(result[1])
            # log and return results
            self.logger.debug("{} received {} from {}".format(caller, message, sender))
            return sender, message
