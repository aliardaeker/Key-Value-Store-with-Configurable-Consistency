import socket
import sys
sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

class Server:
    server_id = sys.argv[1]
    store = {}
    port = int(sys.argv[2])
    ip = socket.gethostbyname(socket.gethostname())
    s_ips = []
    s_ports = []
    s_ids = []
    rangeDict = {}

def partitioner(handler):
    keyRange = 256;
    replicaNumber = len(handler.s_ids)
    for i in replicaNumber:
        handler.rangeDict[i] = [i*(keyRange/replicaNumber),(i+1)*(keyRange/replicaNumber)-1]


def listen(socket, handler):
    while True:
        connection, client = sock.accept()
        try:
            while True:
                data = connection.recv(1024)
                
                if data:
                    pass
                    
                    # if -> get

                    # else if -> put
                        # log first
                        # then update dict_store
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
    log = sys.argv[3]

    # Read .txt for ips and ports of all 4 servers
    with open(servers, 'r') as s:
        for line in s:
            words = line.split()
            if words[0] != server_id:
                try:
                    handler.s_ids.append(words[0])
                    handler.s_ips.append(words[1])
                    handler.s_ports.append(int(words[2]))
                except:
                    print 'File could not read'

    # Check tke log, update the dict_store
    with open(log, 'r') as l:
        for line in l:
            words = line.split()
            try:
                handler.store[int(words[0])] = words[1] 
            except:
                print 'Log could not read'
    
    listen(sock, handler)
