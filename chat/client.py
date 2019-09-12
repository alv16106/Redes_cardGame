import socket
import os
import subprocess


class Client:

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.threads = []
        self.s = socket.socket()
        self.s.connect((host, port))
        self.handle_session()

    def handle_session(self):
        while True:
            data = self.s.recv(1024)
            print(data.decode('utf-8'))
            msg = input('De reversa: ')
            self.s.send(str.encode(msg))


if __name__ == "__main__":
    client = Client(5000, 'localhost')
