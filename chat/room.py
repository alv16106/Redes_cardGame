import socket
import threading
import pickle


class Room:

    def __init__(self, socket, name):
        self.socket = socket
        self.members = []
        self.name = name
        self.threads = []

    def handle_client(self, client):
        clientsocket = client['sock']
        clientsocket.send(str.encode("ls"))
        while True:
            msg = clientsocket.recv(1024)
            # do some checks and if msg == disconnect: break:
            print("recieved in room: ", self.name)
        clientsocket.close()

    def add_user(self, new_client):
        self.members.append(new_client)
        ut = threading.Thread(target=self.handle_client, args=(new_client, ))
        ut.start()
        self.threads.append(ut)
