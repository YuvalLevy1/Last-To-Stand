import json
import threading
import time

from network import network_constants, network_functions

"""
the class is responsible for sending and receiving information in tcp for each client
"""


class Game(threading.Thread):

    def __init__(self, output_sockets, input_sockets, messages):
        """
        :parameter messages is a dictionary that contains tcp socket as a key
        and a message to this socket as a value.
        """
        threading.Thread.__init__(self)
        self.messages = messages
        self.output_sockets = output_sockets
        self.input_sockets = input_sockets
        self.running = False

    """
    the function runs in a different thread.
    it waits for each player to send his tcp update and then sends it to each client.
    sends the clients full update for game info with tcp protocol
    """

    def run(self):
        self.setup_game()
        while self.running:
            time.sleep(network_constants.UPDATE_SPEED)
            message = "update:" + json.dumps(list(self.messages.values()))
            network_functions.send_to_clients(self.output_sockets, message)
            self.messages = self.reset_messages()
        print("end game")

    """
    receives data from each client using udp protocol
    and updates the messages variable according to it.
    """

    def update(self, input_socket, client_id, data):
        if data == "bye":
            self.player_quit(client_id)
        self.messages[input_socket] = data

    def setup_game(self):
        self.running = True
        message = "starting"  # "start" consist of 5 chars
        network_functions.send_to_clients(self.output_sockets, message)
        time.sleep(2)  # for client get "start"

    def player_quit(self, client_id):
        network_functions.send_to_client(self.output_sockets[client_id], "ok")
        self.output_sockets.remove(self.output_sockets[client_id])
        self.messages.remove(self.messages[client_id])
        network_functions.send_to_clients(self.output_sockets, "id disconnected:{} ".format(client_id))

    def reset_messages(self):
        messages = self.messages

        for udp_socket in self.input_sockets:
            messages[udp_socket] = "(0, 0, 'down', False)"
        return messages
