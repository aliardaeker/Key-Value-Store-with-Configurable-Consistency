# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 12:04:09 2018

@author: mohit
"""


# Import socket module
import socket
import sys               
 
ip = sys.argv[1]
port = sys.argv[2]
s = socket.socket()     

s.connect(ip, port)

while True:
    print
    command = raw_input('>>')
    if command:
        if command.strip().split()[0].lower() == 'get':
            key = command.strip().split()[1]
            getReqMessage = store.GetMessage()
            getReqMessage.key = key
            getReqMessage.consistency = 2
            reqMessage = store.RequestMessage()
            reqMessage.get_message.CopyFrom(getReqMessage)
            s.sendall(reqMessage.SerializeToString())
            receiveMessage = store.CoordToClient() 
            received = s.recv(1024)
            receiveMessage.ParseFromString(received)
            print received.value
            
            
        elif command.strip().split()[0].lower() == 'put':
            key = command.strip().split()[1]
            value = command.strip().split()[2]
            
            putReqMessage = store.PutMessage()
            putReqMessage.key = key
            putReqMessage.value = value
            putReqMessage.consistency = 2
            reqMessage = store.RequestMessage()
            reqMessage.put_message.CopyFrom(putReqMessage)
            s.sendall(reqMessage.SerializeToString())
 
           
            
# close the connection
s.close() 