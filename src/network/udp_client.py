import socket

from network import network_constants


class UDPClient:

    def __init__(self, client_id):
        self.client_id = client_id
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_ip = network_constants.SERVER_IP
        self.server_port = network_constants.UDP_PORT_NUMBER + client_id
        self.server_address = (self.server_ip, self.server_port)

    def send(self, msg):
        msg = "".join([str(len(msg)).zfill(network_constants.MSG_LEN), msg.strip()])
        self.client_socket.sendto(msg.encode(), self.server_address)

    def disconnect(self):
        self.send("bye")
        self.client_socket.close()
