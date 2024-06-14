import logging
import random
import time
from constMutex import ENTER, RELEASE, ALLOW

class Process:
    def __init__(self, chan, failure_timeout=5):
        self.channel = chan
        self.process_id = self.channel.join('proc')
        self.all_processes = []
        self.other_processes = []
        self.queue = []
        self.clock = 0
        self.logger = logging.getLogger("vs2lab.lab5.mutex.process.Process")
        self.failure_timeout = failure_timeout
        self.last_heartbeat = {}
        self.failed_processes = set()  # Track failed processes
        self.logged_failures = set()  # Track logged failures

    def __mapid(self, id='-1'):
        if id == '-1':
            id = self.process_id
        return 'Proc_' + chr(65 + self.all_processes.index(id))

    def __cleanup_queue(self):
        self.queue = [msg for msg in self.queue if msg[1] not in self.failed_processes]
        if self.queue:
            self.queue.sort()
            while self.queue and self.queue[0][2] == ALLOW:
                self.queue.pop(0)

    def __request_to_enter(self):
        self.clock += 1
        request_msg = (self.clock, self.process_id, ENTER)
        self.queue.append(request_msg)
        self.__cleanup_queue()
        self.channel.send_to(self.other_processes, request_msg)

    def __allow_to_enter(self, requester):
        self.clock += 1
        msg = (self.clock, self.process_id, ALLOW)
        self.channel.send_to([requester], msg)

    def __release(self):
        if not self.queue:
            return
        assert self.queue[0][1] == self.process_id, 'State error: inconsistent local RELEASE'
        self.queue = [r for r in self.queue[1:] if r[2] == ENTER]
        self.clock += 1
        msg = (self.clock, self.process_id, RELEASE)
        self.channel.send_to(self.other_processes, msg)

    def __allowed_to_enter(self):
        processes_with_later_message = set([req[1] for req in self.queue[1:] if req[1] not in self.failed_processes])
        first_in_queue = self.queue and self.queue[0][1] == self.process_id
        active_other_processes = [p for p in self.other_processes if p not in self.failed_processes]
        all_have_answered = len(active_other_processes) == len(processes_with_later_message)
        return first_in_queue and all_have_answered

    def __receive(self):
        _receive = self.channel.receive_from(self.other_processes, 10)
        if _receive:
            msg = _receive[1]
            self.clock = max(self.clock, msg[0])
            self.clock += 1

            msg_type = "ENTER" if msg[2] == ENTER else "ALLOW" if msg[2] == ALLOW else "RELEASE"
            self.logger.debug("{} received {} from {}.".format(self.__mapid(), msg_type, self.__mapid(msg[1])))

            if msg[2] == ENTER:
                self.queue.append(msg)
                self.__allow_to_enter(msg[1])
            elif msg[2] == ALLOW:
                self.queue.append(msg)
            elif msg[2] == RELEASE:
                if self.queue and self.queue[0][1] == msg[1]:
                    assert self.queue[0][2] == ENTER, 'State error: inconsistent remote RELEASE'
                    self.queue.pop(0)

            self.__cleanup_queue()
            self.last_heartbeat[msg[1]] = time.time()
        else:
            self.logger.warning("{} timed out on RECEIVE.".format(self.__mapid()))

        self.__check_for_failures()

    def __check_for_failures(self):
        current_time = time.time()
        for process in self.other_processes:
            if process in self.failed_processes:
                continue

            if process not in self.last_heartbeat:
                self.last_heartbeat[process] = current_time

            if current_time - self.last_heartbeat[process] > self.failure_timeout:
                self.failed_processes.add(process)
                if process not in self.logged_failures:
                    self.logger.warning("Detected failure of process {}. Ignoring it.".format(self.__mapid(process)))
                    self.logged_failures.add(process)  # Mark failure as logged

                self.queue = [msg for msg in self.queue if msg[1] != process]

    def init(self):
        self.channel.bind(self.process_id)
        self.all_processes = sorted(self.channel.subgroup('proc'), key=int)
        self.other_processes = [p for p in self.all_processes if p != self.process_id]

        self.logger.info("Member {} joined channel as {}.".format(self.process_id, self.__mapid()))

    def run(self):
        while True:
            if len(self.all_processes) > 1 and random.choice([True, False]):
                self.logger.debug("{} wants to ENTER CS at CLOCK {}.".format(self.__mapid(), self.clock))
                self.__request_to_enter()
                while not self.__allowed_to_enter():
                    self.__receive()

                sleep_time = random.randint(0, 2000)
                self.logger.debug("{} enters CS for {} milliseconds.".format(self.__mapid(), sleep_time))
                print(" CS <- {}".format(self.__mapid()))
                time.sleep(sleep_time / 1000)

                print(" CS -> {}".format(self.__mapid()))
                self.__release()
                continue

            if random.choice([True, False]):
                self.__receive()
