import socket
import os
import subprocess
import threading
import pickle
import sys
from menu import menu


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
            msg = pickle.loads(data)
            if msg['code'] == 200:
                print('Welcome to the room!')
                continue
            print(msg['payload']['from'] + '>' + msg['payload']['body'])

    def handle_session(self):
        rooms = pickle.loads(self.s.recv(1024))
        print('Available rooms: ', rooms)
        if not self.nick:
            self.nick = input('Select a nickname: ')
        functions = {
            'cr': self.create_room,
            'jr': self.join_room,
            'rooms': self.get_rooms,
            'whisper': self.send_private,
            'kill': self.kill_player,
            'execute': self.execute_player,
            'send_message': self.send_broadcast,
        }
        self.menuInstance = threading.Thread(target=menu, args=(functions,))
        self.menuInstance.start()
        self.reciever()

    # este lo hizo usted amiguito
    def join_room(self, args):
        # yo creo que deberia ser asi
        self.s.send(
            pickle.dumps(
                {'code': 40, 'payload':
                    {'room': args, 'nick': self.nick}}
            )
        )

    def send_broadcast(self, args):
        msg_dict = {}
        msg_dict['code'] = 0
        msg_dict['payload'] = {'from': self.nick, 'body': args}
        self.s.send(pickle.dumps(msg_dict))

    def send_private(self, args):
        msg = input('Message: ')
        msg_dict = {}
        msg_dict['code'] = 10
        msg_dict['payload'] = {'to': args, 'body': msg}
        self.s.send(pickle.dumps(msg_dict))

    def execute_player(self, args):
        self.s.send(pickle.dumps(
            {'code': 20, 'payload': {'from': self.nick, 'vote': int(args)}}
            ))

    def kill_player(self, args):
        self.s.send(pickle.dumps({'code': 30, 'payload': {'vote': int(args)}}))

    def create_room(self, args):
        s = args.split(' ')
        self.s.send(
            pickle.dumps(
                {'code': 50, 'payload':
                    {'roomname': s[0], 'max_players': int(s[1])}}
            )
        )

    def get_rooms(self, args):
        self.s.send(pickle.dumps({'code': 60, 'payload': 0}))

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    client = Client(port, host)
