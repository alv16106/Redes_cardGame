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

    # este lo hizo usted amiguito
    def join_room(self, args):
        self.s.send(pickle.dumps({'room': args, 'nick': self.nick}))
        # yo creo que deberia ser asi
        # self.s.send(
        #     pickle.dumps(
        #         {'code': 40, 'payload':
        #             {'room': int(args)}}
        #     )
        # )

    def send_private(self, args):
        msg = input('Message: ')
        msg_dict = {}
        msg_dict['code'] = 10
        msg_dict['payload']['from'] = self.nick
        msg_dict['payload']['to'] = args
        msg_dict['payload']['msg'] = msg
        self.s.send(pickle.dumps(msg_dict))

    def execute_player(self, args):
        self.s.send(pickle.dumps(
            {'code': 20, 'payload': {'from': self.nick, 'vote': int(args)}}
            ))

    def kill_player(self, args):
        self.s.send(pickle.dumps({'code': 30, 'payload': {'vote': int(args)}}))

    def create_room(self, args):
        self.s.send(
            pickle.dumps(
                {'code': 50, 'payload':
                    {'roomname': args[0], 'max_players': int(args[1])}}
            )
        )

if __name__ == "__main__":
    client = Client(5001, 'localhost')
