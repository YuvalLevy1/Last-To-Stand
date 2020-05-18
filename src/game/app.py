from game import game_client

game = game_client.Game()
data, id = game.init_game()
print("the data is: {} \n{}".format(data, id))

while True:
    print(game.receive_tcp_from_server())
