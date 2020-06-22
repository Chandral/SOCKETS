def receive_message(client_socket, header_length):
    try:
        message_header = client_socket.recv(header_length)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False
