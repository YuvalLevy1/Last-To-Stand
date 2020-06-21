from network import network_constants


def send_to_clients(sockets, message):
    for socket in sockets:
        send_to_client(socket, message)


def send_to_client(socket, message):
    message_len = str(len(message))
    message = "".join([message_len.zfill(network_constants.UDP_MSG_LEN), message])
    message = message.encode()
    socket.send(message)


def receive(client_socket):
    data_len = client_socket.recv(network_constants.UDP_MSG_LEN)
    data = (client_socket.recv(int(data_len.decode()))).decode()
    return data
