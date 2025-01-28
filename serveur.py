import socket
import threading

# Stocker les clients connectés : {client_socket: username}
clients = {}

# Fonction pour diffuser un message à tous les clients
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:  # Ne pas renvoyer le message à l'expéditeur
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del clients[client_socket]

# Gérer les messages privés
def handle_private_message(sender_socket, target_username, message):
    for client_socket, username in clients.items():
        print(username)
        if username == target_username:
            try:
                client_socket.send(f"[PRIVATE] {clients[sender_socket]}: {message}".encode('utf-8'))
            except:
                client_socket.close()
                del clients[client_socket]
            return
    sender_socket.send(f"User {target_username} not found.".encode('utf-8'))

# Gérer chaque client
def handle_client(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = username
    print(f"{username} joined the chat.")
    broadcast(f"{username} joined the chat.".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/private"):
                # Format: /private username message
                _, target_username, private_message = message.split(" ", 2)
                handle_private_message(client_socket, target_username, private_message)
            else:
                broadcast(f"{username}: {message}".encode('utf-8'), client_socket)
        except:
            print(f"{username} disconnected.")
            broadcast(f"{username} left the chat.".encode('utf-8'))
            client_socket.close()
            del clients[client_socket]
            break

# Configurer le serveur
def start_server(host="127.0.0.1", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server is running on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        client_socket.send("Enter your username:".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
