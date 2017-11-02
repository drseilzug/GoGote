#! /usr/bin/env python3
import socket, json
from GoColor import GoColor
from Player import Player
from Game import Game
# import sys

class GoClient:
    def __init__(self, host="localhost", port=9999, color=None, player=Player()):
        """
        initializes a GoClient that connects the a Go server at host:port
        as player of color. If color = None attempts to spectate
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

        self.color = color
        self.player = player
        self.myMove = False  # flag that allows playing a move

        self.game = Game()

        # sets up connection to GoServer
        self.connect()

    def connect(self):
        """
        attempts to connect to host:port
        sends HelloDict and gets response
        """
        self.sock.connect((self.host, self.port))
        helloDict = {}
        helloDict["player"] = self.player.__dict__
        helloDict["color"] = self.color
        helloData = json.dumps(helloDict)
        self.sock.sendall(helloData.encode())


if __name__ == "__main__":
    blackClient = GoClient(color=GoColor.black, player=Player("drseilzug", "8k"))

# # Create a socket (SOCK_STREAM means a TCP socket)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#     # Connect to server and send data
#     sock.connect((HOST, PORT))
#     while True:
#         data = input('Type some data: ')
#         sock.sendall(bytes(data + "\n", "utf-8"))
#
#         # Receive data from the server and shut down
#         received = str(sock.recv(1024), "utf-8")
#
#         print("Sent:     {}".format(data))
#         print("Received: {}".format(received))
#
#         if data == "exit":
#             break
