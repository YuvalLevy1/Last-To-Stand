import socket
from network import network_constants


class TCPClient:

    def __init__(self):
        self.client_socket = socket.socket()
        self.server_ip = network_constants.SERVER_IP
        self.server_port = network_constants.UDP_PORT_NUMBER
        self.server_address = (self.server_ip, self.server_port)

    def send(self, msg):
        msg = msg.strip()
        print("sending message: {} in tcp protocol".format(msg))
        self.client_socket.send(msg.encode())

    def close_socket(self):
        self.client_socket.close()

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def disconnect(self):
        self.send("bye".rjust(network_constants.MSG_LEN))

