import socket
import threading
import pickle
import utils


class Room:

    def __init__(self, socket, name, max_users):
        self.socket = socket
        self.members = {}
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
            msg = pickle.loads(msg)
            pl = msg['payload']
            if msg['code'] == 0:
                self.broadcast(nick, pl['body'])
            elif msg['code'] == 10:
                self.send_message(nick, pl['body'], pl['to'])
            elif msg['code'] == 20:
                pass
            elif msg['code'] == 30:
                pass
            else:
                m = utils.create_message('SERVER', 'No es posible realizar esta acción')
                clientsocket.send(pickle.dumps(m))
        clientsocket.close()

    def add_user(self, new_client):
        self.members[new_client['nick']] = new_client
        ut = threading.Thread(target=self.handle_client, args=(new_client, ))
        ut.start()
        self.threads.append(ut)

    def broadcast(self, sender, body):
        message = pickle.dumps(utils.create_message(sender, body))
        for user in self.members.values():
            if user['nick'] is not sender:
                user['sock'].send(message)

    def send_message(self, sender, body, to):
        message = pickle.dumps(utils.create_message(sender, body))
        self.members[to]['sock'].send(message)
