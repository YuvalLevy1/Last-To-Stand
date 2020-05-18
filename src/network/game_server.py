import json
import threading
import time

from network import network_constants


class Game(threading.Thread):

    def __init__(self, udp_sockets, messages, players):
        """
        :parameter messages is a dictionary that contains tcp socket as a key
        and a message to this socket as a value.
        """
        threading.Thread.__init__(self)
        self.messages = messages
        self.udp_sockets = udp_sockets
        self.running = False
        self.players = players

    """
    the function responsible for updating the clients using TCP
    sends the clients full update for game info with tcp protocol
    """

    def run(self):
        self.running = True
        message = "starting"  # "start" consist of 5 chars
        self.send_to_clients(message)
        time.sleep(2)  # for client get "start"
        while self.running:
            time.sleep(network_constants.TPC_UPDATE_SPEED)
            message = "".join("update:", self.get_update_data())
            num_str = str(len(message))
            message = "".join([num_str.zfill(network_constants.MSG_LEN), message])
            self.send_to_clients(message)
        print("end game")

    def send_to_clients(self, message):
        for socket in self.messages.keys():
            self.send_to_client(socket, message)

    def update(self, udp_socket, data):
        """
        receives data from udp sockets from each client,
        updates the messages variable.

        :param data: the data collected from the udp_socket variable
        :param udp_socket - server socket of current player
        """
        if data == "Bye":
            message = "Bye"
            self.messages.remove(udp_socket)
            udp_socket.send(message)
            client_id = udp_socket.receive()
            self.send_to_clients("id:{} disconnected".format(client_id))
        else:
            self.messages[udp_socket] = data

    @staticmethod
    def send_to_client(client_socket, message):
        message_len = str(len(message))
        message = "".join([message_len.zfill(network_constants.MSG_LEN), message])
        message = message.encode()
        client_socket.send(message)

    def get_update_data(self):
        data = []
        for i in range(len(self.players)):
            data[i] = self.players[i].get_tcp_info()
        data = str(tuple(data))
        return data
