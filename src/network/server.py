import socket

import select

from network import network_constants, game_server

"""
function responsible for the connection of clients.
the function adds the client's socket to the output_sockets list.
output_sockets: the list that will contain all Output sockets
"""


def tcp_connection_loop(output_sockets):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Helps to system forget server after being offline for 1 second
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind socket to localhost and  PORT_NUMBER
    tcp_server_socket.bind((network_constants.SERVER_IP, network_constants.TCP_PORT_NUMBER))
    try:
        #  starting to wait for clients to connect
        tcp_server_socket.listen(1)
        clients_counter = 0  # the amount of clients connected to server

        """ connection loop """
        print("Server is waiting for clients to connect")
        while clients_counter < network_constants.MAX_NUM_OF_CLIENTS:
            tcp_client_socket, client_address = tcp_server_socket.accept()  # Connected point. Server wait for client
            ip, port = client_address
            print(" Received connection from the address: {}:{}".format(ip, port))
            output_sockets.append(tcp_client_socket)  # moving the tcp socket to the output sockets list

            response = "We need to wait to {} more clients". \
                format(str(network_constants.MAX_NUM_OF_CLIENTS - clients_counter - 1))
            send_to_all_clients(output_sockets, response)
            send_to_client(tcp_client_socket, "id:" + str(clients_counter))  # sending each client his id
            clients_counter = clients_counter + 1
    except Exception as e:
        print("exceptions occurred in clients connection: {}".format(e.args))

    finally:
        tcp_server_socket.close()
        send_to_all_clients(output_sockets, "all clients are connected")
        return output_sockets


""" receiving input from the udp sockets"""


def receive(server_socket):
    try:
        data, client_address = server_socket.recvfrom(network_constants.MSG_LEN)
        data = data.decode()
        data = data.strip()
        print("message From: " + str(client_address) + "  " + data)
        return data, client_address

    except Exception as e:
        print("exception occurred in input {}".format(e.args))
        return None


"""
the function responsible for initializing the clients' udp sockets 
"""


def initialize_udp_sockets():
    udp_sockets = []
    for i in range(network_constants.MAX_NUM_OF_CLIENTS):
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server_socket.bind((network_constants.SERVER_IP, network_constants.UDP_PORT_NUMBER + i))
        udp_sockets.append(udp_server_socket)
    return udp_sockets


"""
the function responsible for closing the clients' udp sockets
"""


def close_sockets(udp_sockets):
    for udp_socket in udp_sockets:
        udp_socket.close()


"""
the function creates the messages variable
according to the amount of clients connected
"""


def create_socket_messages_var(udp_sockets):
    messages = {}
    for udp_socket in udp_sockets:
        messages[udp_socket] = ""
    return messages


def send_to_all_clients(sockets, message):
    for socket in sockets:
        send_to_client(socket, message)


def send_to_client(socket, message):
    message_len = str(len(message))
    message = "".join([message_len.zfill(network_constants.MSG_LEN), message])
    message = message.encode()
    socket.send(message)


def main():
    """
    connection loop
    every client has two threads and two sockets
    one for Input and one for Output
    """
    # Set up the server:
    players = []  # the list of players
    output_sockets = []  # the list of the clients' tcp sockets
    udp_sockets = initialize_udp_sockets()  # the list of the clients' udp sockets
    output_sockets = tcp_connection_loop(output_sockets)  # connecting all clients
    messages = create_socket_messages_var(udp_sockets)  # a dictionary with the socket
    # as a key and message as a value

    try:

        game = game_server.Game(output_sockets, messages)
        game.setDaemon(True)
        game.start()
        running = True
        print("Server Started.")

        while running:
            readable, writable, exceptional = select.select(udp_sockets, [], udp_sockets, 1)

            for udp_server_socket in readable:
                request = None
                try:
                    request, address = receive(udp_server_socket)

                except ConnectionResetError as e:
                    request = None
                    print("connection reset error: {}".format(e.args))
                if request:
                    game.update(udp_server_socket, request)
                    if request == "Bye":
                        print("break")
                        running = False
                        break

    except Exception as e:
        print("2:", e.args)
    finally:
        close_sockets(udp_sockets)


if __name__ == '__main__':
    main()
