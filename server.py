import socket
import sys
sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

class Server:
    dict_store = {}
    port = int(sys.argv[1])
    ip = socket.gethostbyname(socket.gethostname())

def listen(socket, handler):
    while True:
        connection, client = sock.accept()
        try:
            while True:
                data = connection.recv(1024)
                
                if data:
                    pass
                else:
                    break
        finally:
            connection.close()

if __name__ == '__main__':
    handler = Server()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (handler.ip, handler.port);
    sock.bind(server_address)
    sock.listen(1)
    listen(sock, handler)
