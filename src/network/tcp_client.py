import socket
from threading import Thread

from network import network_constants


class TCPClient(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.client_socket = socket.socket()
        self.server_ip = network_constants.SERVER_IP
        self.server_port = network_constants.TCP_PORT_NUMBER
        self.server_address = (self.server_ip, self.server_port)

    def send(self, msg):
        print("sending message: {} in tcp protocol".format(msg))
        msg_len = str(len(msg))
        msg = "".join([msg_len.zfill(network_constants.MSG_LEN), msg])
        self.client_socket.send(msg.encode())

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def disconnect(self):
        self.send("bye".rjust(network_constants.MSG_LEN))
        self.client_socket.close()

    def receive(self):
        data = self.client_socket.recv(network_constants.MSG_LEN)
        data = self.client_socket.recv(int(data.decode()))
        return data.decode()

    def run(self):
        try:
            while True:
                data = self.receive()

        except Exception as e:
            print("exception occurred in tcp reading thread: {}".format(e.args))

        finally:
            self.client_socket.close()
