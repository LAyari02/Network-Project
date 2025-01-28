import socket
import threading

# Fonction pour recevoir des messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from the server.")
            client_socket.close()
            break

# Fonction pour envoyer des messages
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

# Configurer le client
def start_client(host="127.0.0.1", port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Envoyer le nom d'utilisateur
    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))

    # Démarrer les threads pour envoyer et recevoir des messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    send_messages(client_socket)

if __name__ == "__main__":
    start_client()
