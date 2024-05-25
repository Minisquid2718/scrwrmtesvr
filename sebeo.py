import socket
import threading
import os

clients = []

def handle_client(client_socket, client_address):
    print(f"[INFO] Client connected: {client_address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"[INFO] Received from {client_address}: {message.decode()}")
            broadcast_message(message, client_socket)
        except:
            break

    print(f"[INFO] Client disconnected: {client_address}")
    clients.remove(client_socket)
    client_socket.close()

def broadcast_message(message, current_client):
    for client in clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                pass

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', int(os.environ.get("PORT", 12345))))
    server_socket.listen(5)
    print(f"[INFO] Server listening on port {os.environ.get('PORT', 12345)}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
