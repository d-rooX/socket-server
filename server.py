import socket
from select import select
import time


class Server():
    def __init__(self, port=1337, max_clients=5):
        self.srvsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = port
        self.MAX_CLIENTS = max_clients
        self.to_monitor = [self.srvsocket, ]
        self.users = {}

    def server_start(self):
        while True:
            try:
                self.srvsocket.bind(('', self.PORT))
                print(self.PORT)
                break
            except OSError:
                self.PORT += 1
        self.srvsocket.listen(self.MAX_CLIENTS)
        self.event_loop()

    def accept_connections(self):
        user_socket, addr = self.srvsocket.accept()
        self.users[user_socket] = f'{addr[0]}<{user_socket.fileno()}>'
        self.to_monitor.append(user_socket)
        print(f'Connection from {addr}')

    def send_message(self, user_socket):
        request = user_socket.recv(4096)
        if request:
            for user in self.users:
                if not user is user_socket:
                    user.send(f'From {self.users[user]} --> {request.decode()}'.encode())
        else:
            user_socket.close()
            self.users.pop(user_socket)

    def event_loop(self):
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self.srvsocket:
                    self.accept_connections()
                else:
                    self.send_message(sock)


if __name__ == '__main__':
    server = Server()
    server.server_start()
