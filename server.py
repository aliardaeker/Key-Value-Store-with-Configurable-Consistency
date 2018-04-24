import socket
import sys
import os
import thread
sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

class Server:
    def __init__(self, port, replica_file, s_id)
        self.s_id = s_id
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.store = {}
        self.port = port
        self.replicas = {}

        self.log_file = "LOGFILE_" + str(self.s_id) # Name of logfile
        self.replica_file = replica_file #IP and port of other rep
        self.LogFileCheck() #Check log file
        self.server_init() #starts the server

    def server_init(self):
        ## Either wait for client (means I am coord) else wait for other replicas
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (self.server_ip, self.port)
        sock.bind(server_address)
        sock.listen(5) # Need to finish this
        
        try:
            t = thread.start_new_thread(thread_listener, (sock, ))
        except:
            print 'Threads cannot be initiated'

        while True:
            pass
 
    def LogFileCheck(self):
        if os.path.isfile(self.log_file):
            with open(self.log_file, "w") as logfile:
                for line in logfile:
                    key, value, timestamp = line.split()
                    self.store[key] = (value, timestamp)
        else:
            open(self.log_file, 'a').close() # Create file and ignore if it exists

    def ReadFile(self):
        with open(self.replica_file, "r") as replicafile: #Assume it exists
            for line in replicafile:
                info = line.split()
                self.replicas[info[0], (info[1], info[2])]
                    
    def put_request_handler(self, msg, sock):
        key = msg.put_message.key 
        value = msg.put_message.value
        t = msg.put_message.timestamp
        prime_s = key % 4
        consistency = msg.put_message.consistency
        consistency_count = 0

        if prime_s == self.s_id:
            consistency_count+=1
            with open(self.log_file, "a+") as logfile:
                logfile.write(key + ' ' + value + ' ' + t)
            
            self.store[key] = (value, t)      

            replica_list = [(self.s_id+1) % 4, (self.s_id+2) % 4]
        else
            replica_list = [(self.s_id+1) % 4, (self.s_id+2) % 4, (self.s_id+3) % 4]
        
        # Ask to the replicas
        t = thread.start_new_thread(thread_sender, (replica_list, key, value, timestamp, consistency,consistency_count,sock, ))
           
    def thread_sender(self, replica_list, key, value, timestamp, consistency, consistency_count, sock):
        msg_sent = False

        for rep in replica_list:
            if consistency_count == consistency and not msg_sent:
                msg_sent = True
                coord_client_msg = store_pb2.CoordToClient()
                coord_client_msg.status = 1
                req_msg = store_pb2.RequestMessage()
                req_msg.coord_message.CopyFrom(coord_client_msg)
                sock.sendall(req_msg.SerializeToString())
                pass

            ip, port = self.replicas[rep]
            send_socket = socket.socket()
            try:
                send_socket.connect(ip, port)
                put_msg = store_pb2.PutMessageReplica()
                put_msg.key = key
                put_msg.value = value
                put_msg.timestamp = timestamp
                put_msg.consistency = consistency

                req_msg = store_pb2.RequestMessage()
                req_msg.put_message_replica.CopyFrom(req_msg)
                send_socket.sendall(req_msg.SerializeToString())
                recieved_data = send_socket.recv(2048)
                recieved_msg = store_pb2.ReplicaToCoord()
                recieved_msg.ParseFromString(recieved_data)
                if recieved_msg.status == 1:
                    consistency_count+=1
            except:
                pass

        if not msg_sent:
            # send fail to client
            coord_client_msg = store_pb2.CoordToClient()
            coord_client_msg.status = 0
            req_msg = store_pb2.RequestMessage()
            req_msg.coord_message.CopyFrom(coord_client_msg)
            sock.sendall(req_msg.SerializeToString())

    def update_req_from_coord(self, msg, connection):
        key = msg.put_message_replica.key 
        value = msg.put_message_replica.value
        t = msg.put_message_replica.timestamp

        with open(self.log_file, "a+") as logfile:
             logfile.write(key + ' ' + value + ' ' + t)
        self.store[key] = (value, t) 

        put_msg = store_pb2.ReplicaToCoord()
        put_msg.status = 1


        req_msg = store_pb2.RequestMessage()
        req_msg.rep_coord.CopyFrom(put_msg)
        connection.sendall(req_msg.SerializeToString())
        # return succ to coor


    def thread_listener(sock):
        while True:
            connection, client = sock.accept()
            try:
                while True:
                    data = connection.recv(1024)

                    if data:
                        msg = store_pb2.RequestMessage()
                        msg.ParseFromString(data)
                         
                        if msg.request_message.HasField('put_message'):
                            self.put_request_handler(msg, connection)
                        elif msg.request_message.HasField('put_message_replica'):
                            self.update_req_from_coord(msg, connection)
                        elif msg.request_message.HasField('get_message'):
                            pass
                        else 
                            raise Exception('Error in thread listener')
                    
                    else:
                        break
            finally:
                connection.close()

        
if __name__ == '__main__':
    port = sys.argv[2]
    log_file = sys.argv[3]
    handler = Server(port, log_file, sys.argv[1]) 
