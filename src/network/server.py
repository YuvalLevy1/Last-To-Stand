import socket

import select

from network import network_constants, game_server, network_functions

"""
function responsible for the connection of clients.
the function adds the client's socket to the output_sockets list.
output_sockets: the list that will contain all Output sockets
"""


def tcp_connection_loop():
    output_sockets = []

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind((network_constants.SERVER_IP, network_constants.TCP_PORT_NUMBER))

    try:

        #  starting to wait for clients to connect
        tcp_server_socket.listen(1)

        print("Server is waiting for clients to connect")

        for clients_counter in range(network_constants.MAX_NUM_OF_CLIENTS):
            tcp_client_socket, client_address = tcp_server_socket.accept()  # Connected point. Server wait for client
            ip, port = client_address
            print(" Received connection from the address: {}:{}".format(ip, port))
            output_sockets.append(tcp_client_socket)  # moving the tcp socket to the output sockets list

            response = "We need to wait to {} more clients". \
                format(str(network_constants.MAX_NUM_OF_CLIENTS - clients_counter - 1))

            network_functions.send_to_client(tcp_client_socket,
                                             "id:" + str(clients_counter))  # sending each client his id

            network_functions.send_to_clients(output_sockets, response)

            clients_counter = clients_counter + 1
    except Exception as e:
        print("exceptions occurred in clients connection: {}".format(e.args))

    finally:
        tcp_server_socket.close()
        network_functions.send_to_clients(output_sockets, "all clients are connected")
        return output_sockets


def receive(server_socket):
    try:
        data, client_address = server_socket.recvfrom(network_constants.UDP_MSG_LEN)
        data = data.decode().strip()
        return data, client_address

    except Exception as e:
        print("3:", e.args)
        return None


def initialize_udp_sockets():
    udp_sockets = []
    for i in range(network_constants.MAX_NUM_OF_CLIENTS):
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server_socket.bind((network_constants.SERVER_IP, network_constants.UDP_PORT_NUMBER + i))
        udp_sockets.append(udp_server_socket)
    return udp_sockets


"""
the function creates the messages variable
according to the amount of clients connected
"""


def create_socket_messages_var(udp_sockets):
    messages = {}
    for udp_socket in udp_sockets:
        messages[udp_socket] = ""
    return messages


def close_sockets(udp_sockets):
    for udp_socket in udp_sockets:
        if udp_sockets is not None:
            udp_socket.close()


def main():
    """
    connection loop
    every client has two threads and two sockets
    one for Input and one for Output
    """
    # Setting up the server:
    input_sockets = initialize_udp_sockets()  # the list of the clients' udp sockets
    output_sockets = tcp_connection_loop()  # the list of the clients' tcp sockets
    messages = create_socket_messages_var(input_sockets)  # a dictionary with the socket
    # as a key and message as a value

    try:
        game = game_server.Game(output_sockets, messages)
        game.setDaemon(True)
        game.start()
        running = True
        print("Server Started.")
        while running:
            client_id = 0  # the current client's id
            readable, writable, exceptional = select.select(input_sockets, [], input_sockets, 1)
            for udp_server_socket in readable:
                client_id += 1
                request = None
                try:

                    request, address = receive(udp_server_socket)

                    # print(request)
                except ConnectionResetError as e:
                    request = None
                    print("1:", e.args)
                if request:
                    game.update(udp_server_socket, client_id, request)
                    if request == "Bye":
                        input_sockets[client_id] = None
                        running = False
                        break

        # game.join(0)    # close game thread

    except Exception as e:
        print("2:", e.args)

    finally:
        close_sockets(input_sockets)


if __name__ == '__main__':
    main()