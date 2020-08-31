import socket
import threading
import time

server = socket.socket()
server.bind(('', 1337))
server.listen(5)

users = {}


def user_messages_handler(user):
    print(f'Listening {users[user]}')
    while True:
        data = user.recv(2048)
        print(f'\n{users[user]} sent {data}')
        send_all(data, user)


def send_all(data, sender):
    for user in users:
        if not (user is sender):
            user.send(data)


def connection_handler():
    counter = 0
    while True:
        time.sleep(0.1)
        user_socket, address = server.accept()
        users.update({user_socket: f'{address[0]}>{counter}'})
        counter += 1
        user_socket.send('Hello from server!'.encode('utf-8'))
        print(f'User {users[user_socket]} accepted')
        listener = threading.Thread(target=user_messages_handler, args=(user_socket,), name=address[0])
        listener.start()
        print(threading.enumerate())


if __name__ == '__main__':
    connection_handler()