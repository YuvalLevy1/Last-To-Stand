import threading
import time

from game import game_map
from network import network_constants, network_player

"""
the class is responsible for sending and receiving information in tcp for each client
"""


class Game(threading.Thread):

    def __init__(self, tcp_sockets, messages):
        """
        :parameter messages is a dictionary that contains tcp socket as a key
        and a message to this socket as a value.
        """
        threading.Thread.__init__(self)
        self.messages = messages
        self.tcp_sockets = tcp_sockets
        self.players = setup_players()
        self.running = False

    """
    the function runs in a different thread.
    it waits for each player to send his tcp update and then sends it to each client.
    sends the clients full update for game info with tcp protocol
    """

    def run(self):
        self.running = True
        message = "starting"  # "start" consist of 5 chars
        self.send_to_clients(message)
        time.sleep(2)  # for client get "start"
        while self.running:
            time.sleep(network_constants.TPC_UPDATE_SPEED)
            message = "update:" + self.get_update_data()
            num_str = str(len(message))
            message = "".join([num_str.zfill(network_constants.MSG_LEN), message])
            self.send_to_clients(message)
        print("end game")

    def send_to_clients(self, message):
        for socket in self.messages.keys():
            send_to_client(socket, message)

    """
    receives data from each client using udp protocol
    
    """

    def update(self, tcp_socket, data):
        """
        receives data from udp sockets from each client,
        updates the messages variable.

        :param data: the data collected from the udp_socket variable
        :param tcp_socket - server socket of current player
        """

        if data == "Bye":
            message = "Bye"
            self.messages.remove(tcp_socket)
            self.tcp_sockets.remove(tcp_socket)
            tcp_socket.send(message)
            client_id = tcp_socket.receive()
            self.send_to_clients("id:{} disconnected".format(client_id))
        else:
            self.messages[tcp_socket] = data

    def get_update_data(self):
        data = []
        for i in range(len(self.tcp_sockets)):
            data[i] = receive(self.tcp_sockets[i])
        data = str(tuple(data))
        return data


def send_to_client(client_socket, message):
    message_len = str(len(message))
    message = "".join([message_len.zfill(network_constants.MSG_LEN), message])
    message = message.encode()
    client_socket.send(message)


def setup_players():
    players = []
    for i in range(network_constants.MAX_NUM_OF_CLIENTS):
        players.append(network_player.NetworkPlayer(game_map.spawn_points[i][0],
                                                    game_map.spawn_points[i][1],
                                                    game_map.BORDERS,
                                                    i))
    return players


def receive(socket):
    try:
        data = socket.receive(network_constants.MSG_LEN)
        data = data.decode()
        data = data.strip()
        return data

    except Exception as exception:
        print("exception occurred in tcp input {}".format(exception.args))
        return None
