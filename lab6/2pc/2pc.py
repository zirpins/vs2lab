"""
Application performing a distributed commit
- sets up a group of participants
- participants want to jointly commit all of their local
  activities or non at all
- participants and coordinator run in separate processes
- multiprocessing works on unix and windows
"""

import multiprocessing as mp
import logging

import coordinator
import participant
from context import lab_channel, lab_logging

lab_logging.setup(stream_level=logging.INFO, file_level=logging.DEBUG)

logger = logging.getLogger("vs2lab.lab6.2pc.2pc")


def create_and_run(num_bits, proc_class, enter_bar, run_bar):
    """
    Create and run a participant
    :param num_bits: address range of the channel
    :param node_class: class of participant
    :param enter_bar: barrier syncing channel population
    :param run_bar: barrier syncing bootstrap
    """
    chan = lab_channel.Channel(n_bits=num_bits)
    proc = proc_class(chan)
    enter_bar.wait()  # wait for all participants to join the channel
    proc.init()  # do some bootstrapping
    run_bar.wait()  # wait for all nodes to finish
    logger.info(proc.run())  # start operating and log outcome


if __name__ == "__main__":  # if script is started from command line
    m = 8  # Number of bits for process ids
    n = 3  # Number of participants in the group

    # Flush communication channel
    chan = lab_channel.Channel()
    chan.channel.flushall()

    # we need to spawn processes for support of windows
    mp.set_start_method('spawn')

    # create barriers to synchonize bootstrapping
    bar1 = mp.Barrier(n+1)  # Wait for channel population to complete
    bar2 = mp.Barrier(n+1)  # Wait for process-group init to complete

    # start n participants in separate processes
    participants = []
    for i in range(n):
        participant_proc = mp.Process(
            target=create_and_run,
            name="Participant-" + str(i),
            args=(m, participant.Participant, bar1, bar2))
        participants.append(participant_proc)
        participant_proc.start()

    # start coordinator in separate process
    coordinator_proc = mp.Process(
        target=create_and_run,
        name="Coordinator",
        args=(m, coordinator.Coordinator, bar1, bar2))
    coordinator_proc.start()

    # wait for coordinator to finish
    coordinator_proc.join()

    # wait for participants to finish
    for participant_proc in participants:
        participant_proc.join()
