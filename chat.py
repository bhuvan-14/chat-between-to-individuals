import socket
import threading

def receive_messages(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{username}: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def start_chat(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()

    print(f"Server is listening on {ip}:{port}")

    clients = []

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection established with {client_address}")

        username = client_socket.recv(1024).decode('utf-8')
        clients.append((client_socket, username))

        threading.Thread(target=receive_messages, args=(client_socket, username)).start()

def connect_to_server(ip, port, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(username.encode('utf-8'))

    threading.Thread(target=receive_messages, args=(client, username)).start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 12345

    username1 = input("Enter username for person 1: ")
    username2 = input("Enter username for person 2: ")

    threading.Thread(target=start_chat, args=(ip, port)).start()

    connect_to_server(ip, port, username1)
    connect_to_server(ip, port, username2)
