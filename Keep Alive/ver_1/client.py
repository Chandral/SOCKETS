import socket

IP = '127.0.0.1'
PORT = 1234
test_message = "Message sent from the client."

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

while True:
    client_socket.send(test_message.encode('utf-8'))
    print(client_socket.recv(16).decode('utf-8'))
    test_message = input("Send Again? ")