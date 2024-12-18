""" 
Application with a critical section (CS)
- sets up a group of peers 
- peers compete for some critical section
- peers run in separate processes
- multiprocessing should work on unix and windows
- terminates a random process to simulate a crash fault
"""

import sys
import time
import logging
import random
import multiprocessing as mp

from process import Process

from context import lab_channel, lab_logging
from constMutex import BEHAVIOR_TYPES

lab_logging.setup(stream_level=logging.INFO, file_level=logging.DEBUG)

logger = logging.getLogger("vs2lab.lab5.mutex.doit")


def create_and_run(num_bits, peer_name, peer_type, proc_class, enter_bar, run_bar):
    """
    Create and run a peer
    :param num_bits: address range of the channel
    :param peer_name: original name of the peer
    :param peer_type: behavior type of the peer
    :param node_class: class of peer
    :param enter_bar: barrier syncing channel population 
    :param run_bar: barrier syncing bootstrap
    """
    chan = lab_channel.Channel(n_bits=num_bits)
    proc = proc_class(chan)
    enter_bar.wait()  # wait for all peers to join the channel
    proc.init(peer_name, peer_type)  # do some bootstrapping
    run_bar.wait()  # wait for all nodes to finish
    proc.run()  # start operating


if __name__ == "__main__":  # if script is started from command line
    m = 8  # Number of bits for process ids
    n = 4  # Number of processes in the group

    # Check for command line parameters m, n.
    if len(sys.argv) > 2:
        m = int(sys.argv[1])
        n = int(sys.argv[2])

    # Flush communication channel
    chan = lab_channel.Channel()
    chan.channel.flushall()

    # we need to spawn processes for support of windows
    mp.set_start_method('spawn')

    # create barriers to synchonize bootstrapping
    bar1 = mp.Barrier(n)  # Wait for channel population to complete
    bar2 = mp.Barrier(n)  # Wait for process-group init to complete

    # start n competing peers in separate processes
    children: list = []
    for i in range(n):
        peer_name = "Peer-" + str(i)
        peer_type = random.choice(BEHAVIOR_TYPES)
        peer_proc = mp.Process(
            target=create_and_run,
            name=peer_name,
            args=(m, peer_name, peer_type, Process, bar1, bar2))
        children.append((peer_proc, peer_type))
        logger.info("Starting process {} of type {}.".format(
            peer_proc.name, peer_type))
        peer_proc.start()

    # terminate a random process after some time (10 seconds)
    time.sleep(10)
    proc_id = random.randint(0, len(children) - 1)
    proc_to_crash = children[proc_id][0]
    type_to_crash = children[proc_id][1]
    del children[proc_id]

    proc_to_crash.terminate()
    proc_to_crash.join()

    logger.warning("Process {} of type {} has crashed.".format(
        proc_to_crash.name, type_to_crash))

    # wait for peer procs to finish
    for peer_proc in children:
        peer_proc[0].join()
