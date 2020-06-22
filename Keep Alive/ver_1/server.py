import socket

IP = '127.0.0.1'
PORT = 1234
BUFFER = 10
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(10)
list_of_client_sockets = [server_socket]
print(f"Listening for incoming connections @ {IP}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Established connection with {client_address}")
    if client_socket not in list_of_client_sockets:
        list_of_client_sockets.append(client_socket)
    while True:
        received_message = client_socket.recv(BUFFER).decode('utf-8')
        while '.' not in received_message:
            received_message += client_socket.recv(BUFFER).decode('utf-8')
        print(client_address, received_message)
        client_socket.send("Received message".encode('utf-8'))
