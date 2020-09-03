import socket
import selectors


class Server:
    def __init__(self, port=11337, max_clients=5):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = port
        self.MAX_CLIENTS = max_clients
        self.users = {}
        self.selector = selectors.DefaultSelector()
        self.selector.register(fileobj=self.server_socket, events=selectors.EVENT_READ, data=self.accept_connection)

    def server_start(self):
        while True:
            try:
                self.server_socket.bind(('0.0.0.0', self.PORT))
                print(self.PORT)
                break
            except OSError:
                self.PORT += 1
        self.server_socket.listen(self.MAX_CLIENTS)
        self.event_loop()

    def accept_connection(self):
        user_socket, addr = self.server_socket.accept()
        self.users[user_socket] = f'{addr[0]}<{user_socket.fileno()}>'
        self.selector.register(fileobj=user_socket, events=selectors.EVENT_READ, data=self.relay_message)
        print(f'Connection from {addr}')

    def relay_message(self, user_socket):
        request = user_socket.recv(4096)
        if request:
            for user in self.users:
                if not user is user_socket:  # todo: fix
                    user.send(f'{self.users[user_socket]}: {request.decode("utf8")}'.encode('utf8'))
        else:
            print(self.users[user_socket], 'disconnected')
            self.users.pop(user_socket)
            self.selector.unregister(user_socket)
            user_socket.close()

    def event_loop(self):
        while True:
            events = self.selector.select()  # (key, events)
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


if __name__ == '__main__':
    server = Server()
    server.server_start()
