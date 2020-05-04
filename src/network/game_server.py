import time
import json
import threading
from network import network_constants


class Game(threading.Thread):

    def __init__(self, udp_sockets, messages):
        """
        :parameter messages is a dictionary that contains socket as a key
        and a message to this socket as a value.
        """
        threading.Thread.__init__(self)
        self.messages = messages
        self.udp_sockets = udp_sockets

    # overriding threading.Thread's run method
    def run(self):
        pass

    def send_to_clients(self, message):
        message_len = str(len(message))
        message = "".join([message_len.zfill(network_constants.MSG_LEN), message])
        message = message.encode()
        for socket in self.messages.keys():
            socket.send(message)

