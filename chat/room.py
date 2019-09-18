import socket
import threading
import pickle
import utils
import game.cards as cards
from game.main_client import Game


class Room:

    def __init__(self, socket, name, max_users):
        self.socket = socket
        self.members = {}
        self.name = name
        self.threads = []
        self.max = max_users
        self.roles = {'mafia': 'evil', 'town': 'good'}
        self.game = Game(
                        self.max,
                        self.roles,
                        {},
                        self.broadcast,
                        self.send_message)

    def handle_client(self, client):
        nick = client['nick']
        clientsocket = client['sock']
        clientsocket.send(pickle.dumps({'code': 200, 'payload': 'ok'}))
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
                if self.game.IN_GAME and self.game.current_stage == 'EXECUTE':
                    a_s, alive = cards.alive_users(self.game.ASSIGNED_PLAYERS)
                    self.game.VOTES.append(pl['vote']) if nick in alive else None
                    continue
                m = utils.create_msg('SERVER', 'Not yet...')
                clientsocket.send(pickle.dumps(m))
            elif msg['code'] == 30:
                if self.game.IN_GAME and self.game.current_stage == 'NIGHT':
                    a_s, alive = cards.alive_users(self.game.ASSIGNED_PLAYERS)
                    if nick in alive and nick in d:
                        self.game.VOTES.append(pl['vote'])
                        
                    continue
                m = utils.create_msg('SERVER', 'Not yet...')
                clientsocket.send(pickle.dumps(m))
            else:
                m = utils.create_msg('SERVER', 'You can not do this here')
                clientsocket.send(pickle.dumps(m))
        clientsocket.close()

    def add_user(self, client):
        if len(self.members) == self.max:
            response = utils.create_msg('SERVER', 'Room already full')
            client['sock'].send(pickle.dumps(response))
        else:
            self.members[client['nick']] = client
            ut = threading.Thread(target=self.handle_client, args=(client, ))
            ut.start()
            self.threads.append(ut)
            if len(self.members) == self.max:
                self.start_game()

    def start_game(self):
        self.game.IN_GAME = 1
        theboys = cards.generate_roles(self.members.keys(), self.roles)
        self.game.ASSIGNED_PLAYERS = theboys
        game_thread = threading.Thread(target=self.game.run, args=())
        game_thread.start()
        self.broadcast('SERVER', 'GAME READY TO START!')

    def broadcast(self, sender, body):
        message = pickle.dumps(utils.create_msg(sender, body))
        for user in self.members.values():
            if user['nick'] is not sender:
                user['sock'].send(message)

    def send_message(self, sender, body, to):
        message = pickle.dumps(utils.create_msg(sender, body))
        self.members[to]['sock'].send(message)
