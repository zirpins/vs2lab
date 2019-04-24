from context import lab_channel
import logging


class Server:
    def __init__(self):
        self.ci = lab_channel.Channel()
        self.server = self.ci.join('server')
        self.timeout = 3

        # create instance logger
        self.logger = logging.getLogger('vs2lab.lab2.channel.Server')
        self.logger.debug('New Server created.')

    def run(self):
        self.ci.bind(self.server)
        while True:
            message = self.ci.receive_from_any(self.timeout)
            if message is not None:
                try:
                    self.ci.send_to({message[0]}, 'Received ' + message[1])
                except AssertionError:
                    self.logger.warning('Client has already left the channel.')


class Client:
    def __init__(self):
        self.ci = lab_channel.Channel()
        self.client = self.ci.join('client')
        self.server = self.ci.subgroup('server')

        # create instance logger
        self.logger = logging.getLogger('vs2lab.lab2.channel.Client')
        self.logger.debug('New Client created.')

    def run(self):
        self.ci.bind(self.client)
        self.ci.send_to(self.server, 'Hello says ' + self.client)
        answer = self.ci.receive_from(self.server)
        print("Got answer {} from {}.".format(answer[1], answer[0]))
        self.ci.leave('client')
