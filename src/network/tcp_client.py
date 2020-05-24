import socket
from threading import Thread

from network import network_constants, network_functions

"""
the class TCPClient is responsible for connecting to the server
and receiving the tcp updates from it.
"""


class TCPClient(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.server_ip = network_constants.SERVER_IP
        self.server_port = network_constants.TCP_PORT_NUMBER
        self.server_address = (self.server_ip, self.server_port)
        self.client_socket = socket.socket()
        self.game = game  # game_client variable for the player

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def receive(self):
        return network_functions.receive(self.client_socket)

    """
    the target method for the thread.
    responsible for receiving data in tcp protocol from the server
    """

    def run(self):
        try:
            while True:
                data = self.receive()
                if data != "nothing":
                    if data == "ok":
                        self.client_socket.close()
                    else:
                        self.game.tcp_update(data)
        except Exception as exception:
            print("exception occurred in tcp reading thread: {}".format(exception.args))

        finally:
            self.client_socket.close()
