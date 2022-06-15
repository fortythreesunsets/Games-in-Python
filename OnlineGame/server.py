# Run this script first
# Change the configuration at the top right corner to server to run this script

import socket
from _thread import *
from game import Game
import pickle

# get the IPv4 address from cmd -> ipconfig
# the server script has to be running in the machine that has this IP
server = "192.168.0.10"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server started")

connected = set()
games = {}
id_count = 0


def threaded_client(conn, player, game_id):
    global id_count
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            # Check if the match still exists. When one client disconnects, the match is deleted
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_went()
                    elif data != "get":
                        game.play(player, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing match", game_id)
    except:
        pass
        id_count -= 1
        conn.close()


while True:
    conn, addr = s.accept()  # Client accepts connection
    print("Connected to: ", addr)

    id_count += 1
    player = 0
    game_id = (id_count - 1) // 2  # Keep track of the number of matches between 2 players
    if id_count % 2 == 1:  # Create a new match for a player not in a match (matches are between 2)
        games[game_id] = Game(game_id)
        print("Creating a new match...")
    else:
        games[game_id].ready = True
        player = 1

    start_new_thread(threaded_client, (conn, player, game_id))
