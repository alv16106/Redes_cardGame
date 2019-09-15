import socket
import os
import subprocess
import pickle


class Client:

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.threads = []
        self.s = socket.socket()
        self.s.connect((host, port))
        self.handle_session()

    def handle_session(self):
        rooms = pickle.loads(self.s.recv(1024))
        print('Available rooms: ', rooms)
        room = input('Select room: ')
        nickname = input('Select a nickname: ')
        self.s.send(pickle.dumps({'room': room, 'nick': nickname}))
        while True:
            data = self.s.recv(1024)
            print(data.decode('utf-8'))
            msg = input('De reversa: ')
            self.s.send(str.encode(msg))


if __name__ == "__main__":
    client = Client(5001, 'localhost')
