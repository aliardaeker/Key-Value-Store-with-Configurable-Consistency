# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 12:04:09 2018

@author: mohit
"""


# Import socket module
import socket
import datetime
import sys
import time

def contact_coord(split_command):

    key = split_command[1]

    if split_command[0].lower() == "get":

        getReqMessage = store.GetMessage()
        getReqMessage.key = key
        getReqMessage.consistency = 2

        getReqMessage.timestamp = time.mktime(datetime.datetime.today().timetuple())
        reqMessage = store.RequestMessage()
        reqMessage.get_message.CopyFrom(getReqMessage)
        s.sendall(reqMessage.SerializeToString())
        receiveMessage = store.CoordToClient() 
        received = s.recv(1024)
        receiveMessage.ParseFromString(received)
        print received.value
    
    elif command.split()[0].lower() == 'put':
        value = command.split()[2]
            
        putReqMessage = store.PutMessage()
        putReqMessage.key = key
        putReqMessage.value = value
        putReqMessage.consistency = 2

        putReqMessage.timestamp = time.mktime(datetime.datetime.today().timetuple())
        reqMessage = store.RequestMessage()
        reqMessage.put_message.CopyFrom(putReqMessage)
        s.sendall(reqMessage.SerializeToString())

            # Will recieve status and stuff
    


def correct_format():
    print "For Get Requests - get <key>"
    print "For Put Requests - put <key> <value>"



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Enter the correct number of arguments!"
        exit()
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket()     

    s.connect(ip, port)

    correct_format()

    while True:
        command = raw_input('>>')
        if command:

            try:
                user_command = command.split()
                if (len(user_command) < 2) or (len(user_command) > 3):
                    correct_format()
                contact_coord(user_command)
            except:
                print "Unable to read, please follow \n"
                correct_format()

            
    
            
                
    # close the connection
    s.close() 