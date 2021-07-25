import threading
import socket

nickname = input("Enter nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 55556
client.connect((host, port))


def receive_msg():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("An error occurred!!")
            client.close()
            break


def write_msg():
    while True:
        text = input(">>>")
        client.send(f"{nickname}: {text}".encode())


t1 = threading.Thread(target=receive_msg)
t1.start()
t2 = threading.Thread(target=write_msg)
t2.start()
