import threading
import socket

host = '127.0.0.1'
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick = nicknames[index]
            nicknames.remove(nick)
            print(f'{nick} is disconnected.')
            broadcast(f"{nick} left the chat.".encode())
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"{address} is now connected.")

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast(f"{nickname} has joined the chat!!".encode())
        client.send("Yor are connected to the server.".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
