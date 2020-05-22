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
        self.running = False

    """
    the function runs in a different thread.
    it waits for each player to send his tcp update and then sends it to each client.
    sends the clients full update for game info with tcp protocol
    """

    def run(self):
        self.setup_game()
        while self.running:
            time.sleep(network_constants.TPC_UPDATE_SPEED)
            message = "update:" + self.get_update_data()
            send_to_clients(self.tcp_sockets, message)
        print("end game")

    """
    receives data from each client using udp protocol
    and updates the messages variable according to it.
    """

    def update(self, udp_socket, data):
        self.messages[udp_socket] = data

    def get_update_data(self):
        data = []
        for i in range(len(self.tcp_sockets)):
            data[i] = receive(self.tcp_sockets[i])
        data = str(tuple(data))
        return data

    def setup_game(self):
        self.running = True
        message = "starting"  # "start" consist of 5 chars
        send_to_clients(self.tcp_sockets, message)
        time.sleep(2)  # for client get "start"
        players = setup_players()
        data = []
        for i in range(len(players)):
            data[i] = players[i].get_info_tcp()
        send_to_clients(self.tcp_sockets, str(data))


def send_to_client(client_socket, message):
    message_len = str(len(message))
    message = "".join([message_len.zfill(network_constants.MSG_LEN), message])
    message = message.encode()
    client_socket.send(message)


def send_to_clients(clients_socket, message):
    for socket in clients_socket:
        send_to_client(socket, message)


def receive(socket):
    try:
        data_len = socket.receive(network_constants.MSG_LEN)
        data_len = data_len.decode()
        data = socket.receive(data_len)
        data = data.strip()
        return data

    except Exception as exception:
        print("exception occurred in tcp input {}".format(exception.args))
        return None


def setup_players():
    players = []
    for i in range(network_constants.MAX_NUM_OF_CLIENTS):
        players.append(network_player.NetworkPlayer(game_map.spawn_points[i][0],
                                                    game_map.spawn_points[i][1],
                                                    game_map.BORDERS,
                                                    i))
    return players


def player_quit(client_id):
    send_to_clients("id:{} disconnected".format(client_id))
