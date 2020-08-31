import socket
import threading

client = socket.socket()
client.connect(('127.0.0.1', 1337))


def messages_handler():
    while True:
        data = client.recv(2048).decode('utf-8')
        print(f'\n{data}')


if __name__ == '__main__':
    handler = threading.Thread(target=messages_handler)
    handler.start()
    while True:
        client.send(input().encode('utf-8'))