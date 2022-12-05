import socket
import threading


host = '127.0.0.1'
port = 42069

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(4200)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast('{} left!'.format(name).encode('ascii'))
            names.remove(name)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICK'.encode('ascii'))
        name = client.recv(4200).decode('ascii')
        names.append(name)
        clients.append(client)
        print("Name is {}".format(name))
        broadcast("{} joined!".format(name).encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

