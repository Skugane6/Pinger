from socket import *
import sys

server_socket = socket(AF_INET, SOCK_STREAM)
server_port = 6789

try:
    server_socket.bind(('172.30.160.67', server_port))
    server_socket.listen(1)
    print('Server is ready...')

    while True:
        print('Waiting for incoming connections...')
        connection_socket, address = server_socket.accept()
        try:
            request_message = connection_socket.recv(1024).decode()
            requested_file = request_message.split()[1]
            file = open(requested_file[1:])
            
            connection_socket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

            for data in file.read():
                connection_socket.send(data.encode())
            
            connection_socket.send("\r\n".encode())
            connection_socket.close()
        except IOError:
            connection_socket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            connection_socket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
            connection_socket.close()
except OSError as error:
    print(f"Error: {error}")
finally:
    server_socket.close()
    sys.exit()