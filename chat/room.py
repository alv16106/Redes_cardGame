import socket
import threading
import pickle
import utils


class Room:

    def __init__(self, socket, name, max_users):
        self.socket = socket
        self.members = []
        self.name = name
        self.threads = []
        self.max = max_users

    def handle_client(self, client):
        nick = client['nick']
        clientsocket = client['sock']
        clientsocket.send(pickle.dumps({'code': 0, 'payload': 'ok'}))
        while True:
            msg = clientsocket.recv(1024)
            if not msg:
                break
            # do some checks and if msg == disconnect: break:
            print("recieved in room: ", self.name)
            self.broadcast(nick, msg)
        clientsocket.close()

    def add_user(self, new_client):
        self.members.append(new_client)
        ut = threading.Thread(target=self.handle_client, args=(new_client, ))
        ut.start()
        self.threads.append(ut)

    def broadcast(self, sender, body):
        message = pickle.dumps(utils.create_message(sender, body))
        for user in self.members:
            if user['nick'] is not sender:
                user['sock'].send(message)
