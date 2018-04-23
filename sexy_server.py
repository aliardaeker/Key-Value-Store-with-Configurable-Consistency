import socket
import sys
import os
# sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

class Server:

    def __init__(self, server_id, port, replica_file)
        self.server_id = server_id
        self.store = {}
        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname())
        self.s_ips = []
        self.s_ports = []
        self.s_ids = []
        self.rangeDict = {}
        self.log_file = "LOGFILE" #Name of logfile
        self.replica_file = replica_file #IP and port of other rep
        self.LogFileCheck() #Check log file
        self.server_init() #starts the server

    def server_init(self):
        ## Either wait for client (means I am coord) else wait for other replicas
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('', self.port)
        sock.bind(server_address)
        sock.listen(5) ##Need to finish this

        sock.accept()


    def LogFileCheck(self):
        if os.path.isfile(self.log_file):
                with open(self.log_file, "w") as logfile:
                    for line in logfile:
                        key, value, timestamp = line.split()
                        self.store[key] = value
        else:
                open(self.log_file, 'a').close() # Create file and ignore if it exists

    def ReadFile(self):
        with open(self.replica_file, "r") as replicafile: #Assume it exists
            for line in replicafile:
                info = line.split()
                self.s_ids.append(info[0])
                self.s_ips.append(info[1])
                self.s_ports.append(int(info[2]))

    def partitioner(handler):
        keyRange = 256;
        replicaNumber = len(self.handler.s_ids)
        for i in replicaNumber:
            self.rangeDict[i] = [i*(keyRange/replicaNumber),(i+1)*(keyRange/replicaNumber)-1]


    # def listen(socket, handler):
    #     while True:
    #         connection, client = sock.accept()
    #         try:
    #             while True:
    #                 data = connection.recv(1024)
                    
    #                 if data:
    #                     pass
                        
    #                     # if -> get

    #                     # else if -> put
    #                         # log first
    #                         # then update dict_store
    #                 else:
    #                     break
    #         finally:
    #             connection.close()

if __name__ == '__main__':
    server_id = sys.argv[1]
    port = sys.argv[2]
    log_file = sys.argv[3]

    handler = Server(server_id, port, log_file)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (handler.ip, handler.port);
    sock.bind(server_address)
    sock.listen(3)

    # # Read .txt for ips and ports of all 4 servers
    # with open(servers, 'r') as s:
    #     for line in s:
    #         words = line.split()
    #         if words[0] != server_id:
    #             try:
    #                 handler.s_ids.append(words[0])
    #                 handler.s_ips.append(words[1])
    #                 handler.s_ports.append(int(words[2]))
    #             except:
    #                 print 'File could not read'

    # # Check tke log, update the dict_store
    # with open(log, 'r') as l:
    #     for line in l:
    #         words = line.split()
    #         try:
    #             handler.store[int(words[0])] = words[1] 
    #         except:
    #             print 'Log could not read'
    
    # listen(sock, handler)
