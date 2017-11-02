#! /usr/bin/env python3
import socket
import threading
import json
from Game import Game
from GoColor import GoColor
# from GoColor import GoColor

global QUIT
QUIT = False


class GoServer(threading.Thread):
    def __init__(self, host='localhost', port=9999, connections=10, game=Game()):
        print("__init__")
        super().__init__()
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientBlack = None
        self.clientWhite = None
        self.clientSpecs = {}  # current connections

        # setup a generic game
        self.setupGame(game)

        self.server.bind((host, port))  # TODO try for socket exceptions

        self.server.listen(connections)

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, *args):
        print("__exit__")
        self.server.close()

    def setupGame(self, game=Game()):
        """
        initializes a Game on the server
        """
        self.game = game

    def run_thread(self, conn, addr):
        # connect to client
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        # recive client 'hello' information dict as JSON:
        # color :: GoColor of desired player or None if spectator
        # player :: __dict__
        helloData = conn.recv(1024)
        helloDict = json.loads(helloData.decode())

        # register playersockets or spectatorsockets to server
        valid = True
        if helloDict["color"] == GoColor.black:
            if self.clientBlack is None:
                self.clientBlack = (conn, addr)
            else:
                valid = False
        elif helloDict["color"] == GoColor.white:
            if self.clientWhite is None:
                self.clientWhite = (conn, addr)
            else:
                valid = False
        elif helloDict["color"] is None:
            self.clientSpecs.append(conn, addr)
        else:
            raise ValueError("invalid Color Signature: "+helloDict["color"])
        if not valid:
            pass  # TODO somehow tell client it f*ed up and how
        

        conn.close()  # Close

    def clientLoop(self, conn, color):
        pass

    def specLoop(self, conn):
        pass

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.run_thread, args=(conn, addr)).start()

    def getGameJSON(self):
        pass


if __name__ == "__main__":
    with GoServer("", 9999) as server:
        server.start()
        while not QUIT:
            pass
