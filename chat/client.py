import socket
import os
import subprocess
import threading
import pickle


class Client:

    def __init__(self, port, host, nick=''):
        self.port = port
        self.host = host
        self.nick = nick
        self.threads = []
        self.s = socket.socket()
        self.s.connect((host, port))
        self.handle_session()

    def reciever(self):
        while True:
            data = self.s.recv(1024)
            print(pickle.loads(data))

    def handle_session(self):
        rooms = pickle.loads(self.s.recv(1024))
        print('Available rooms: ', rooms)
        room = input('Select room: ')
        if not self.nick:
            self.nick = input('Select a nickname: ')
        self.s.send(pickle.dumps({'room': room, 'nick': self.nick}))
        nt = threading.Thread(target=self.reciever, args=())
        nt.start()
        while True:
            msg = input('envie algo: ')
            self.s.send(str.encode(msg))


if __name__ == "__main__":
    client = Client(5001, 'localhost')
