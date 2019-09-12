import socket
import threading


class Server:

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.connections = []
        self.address = []
        self.threads = []
        self.s = socket.socket()
        self.s.bind((host, port))
        self.s.listen(5)
        self.accepting_connections()

    def handle_client(self, clientsocket, addr):
        clientsocket.send(str.encode("ls"))
        while True:
            msg = clientsocket.recv(1024)
            # do some checks and if msg == disconnect: break:
            print("recieved")
        clientsocket.close()

    def accepting_connections(self):
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
            self.threads.append(threading.Thread(target=self.handle_client, args=(conn, address)))
            self.threads[-1].start()


if __name__ == "__main__":
    server = Server(5000, "localhost")
