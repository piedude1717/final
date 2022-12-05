import socket
import threading

name = input("Choose your Name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 42069))


def receive():
    while True:
        try:
            message = client.recv(4200).decode('ascii')
            if "/q" in message:
                client.close()
                print(name, " has left the chat.")
                break

            elif message == 'NICK':
                client.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print("An error has occurred!")
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(name, input(''))
        if "/q" in message:
            client.close()
            print(name, "has left the chat.")
            break
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

