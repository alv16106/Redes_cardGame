import socket
import threading
import pickle
import room
import utils


class Server:

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.connections = []
        self.address = []
        self.threads = []
        self.rooms = {}
        self.s = socket.socket()
        self.s.bind((host, port))
        self.s.listen(5)
        self.accepting_connections()

    def handle_new(self, c_sock, addr):
        c_sock.send(pickle.dumps([*self.rooms]))
        while True:
            msg = c_sock.recv(1024)
            if not msg:
                break
            # do some checks and if msg == disconnect: break:
            msg = pickle.loads(msg)
            print(msg)
            pl = msg['payload']
            if msg['code'] == 40:
                if pl['room'] in self.rooms:
                    user = {'nick': pl['nick'], 'sock': c_sock, 'addr': addr}
                    self.rooms[pl['room']].add_user(user)
                    break
                else:
                    message = pickle.dumps(utils.create_message('SERVER', 'Room not existant'))
                    c_sock.send(message)
            elif msg['code'] == 50:
                pl = msg['payload']
                self.create_room(pl['roomname'], pl['max_players'])
            else:
                message = pickle.dumps(utils.create_message('SERVER', 'No es posible realizar esta acción'))
                c_sock.send(message)
        # do some checks and if msg == disconnect: break:

    def create_room(self, name, max_users):
        print(self.rooms, ' rooms available')
        self.rooms[name] = room.Room(self.s, name, max_users)

    def accepting_connections(self):
        self.create_room('first', 5)
        self.create_room('second', 5)
        for c in self.connections:
            c.close()

        del self.connections[:]
        del self.address[:]

        while True:
            conn, address = self.s.accept()
            self.s.setblocking(1)  # prevents timeout

            self.connections.append(conn)
            self.address.append(address)
            print("Connection has been established :" + address[0])
            nt = threading.Thread(target=self.handle_new, args=(conn, address))
            nt.start()
            self.threads.append(nt)
        self.s.close()


if __name__ == "__main__":
    server = Server(5000, "localhost")
