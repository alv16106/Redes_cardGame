import socket
import threading
import pickle
import room


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

    def handle_new(self, clientsocket, addr):
        clientsocket.send(pickle.dumps([*self.rooms]))
        msg = pickle.loads(clientsocket.recv(1024))
        # do some checks and if msg == disconnect: break:
        if msg['room'] in self.rooms:
            user = {'nick': msg['nick'], 'sock': clientsocket, 'addr': addr}
            self.rooms[msg['room']].add_user(user)

    def create_room(self, name):
        print(self.rooms, ' rooms available')
        self.rooms[name] = room.Room(self.s, name)

    def accepting_connections(self):
        self.create_room('first')
        self.create_room('second')
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
    server = Server(5001, "localhost")
    server.create_room('first')
    server.create_room('second')
