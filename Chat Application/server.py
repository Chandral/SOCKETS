import socket
import select
import helper as h

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(10)

sockets_list = [server_socket]
clients = {}

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = h.receive_message(client_socket, HEADER_LENGTH)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"Accepted new connection from {client_address} usernam:{user['data'].decode('utf-8')}")
        else:
            message = h.receive_message(notified_socket, HEADER_LENGTH)
            if not message:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {user['header'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
