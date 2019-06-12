import socket
from DataBase import DataBase

class SocketManager():
    def __init__(self,port):
        self.port = port
        self.clients = {}
        self.names = {}
        self.clientsAdresess = []
        
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',self.port))
        self.server.listen(10)    

    def accept(self):
        return self.server.accept()

    def broadcast(self,l):
        temp = self.clients #to prevent problems
        counter = 0
        for clientSocket in temp.keys(): #send to all the clients the music
            try:
                if temp[clientSocket]:
                    clientSocket.send(l)
            except: #if one of the clients is not connected anymore delete it
                self.remove_user(clientSocket,counter)
                counter = counter+1

    def remove_user(self,clientSocket,counter):
            print "good bye " + str(self.clientsAdresess[counter])
            del self.clients[clientSocket]
            del self.names[clientSocket]
            del self.clientsAdresess[counter]
        
    def listen_to_clients(self,client,data):
        while True:
            try:
                x = client.recv(1024)
                print x
                if "Connection:" in x: #check if he is trying to connect
                    x = x.split(":")
                    x = x[-1].split(",")                    
                    name = x[0]
                    password = x[-1]
                    m = data.check_login(name,password,self.names)
                    if m == "Connection accepted":
                        self.clients[client]=True
                        self.names[client]=name
                    client.send(m)
                elif "Disconnect:" in x: #check if he want to disconnect
                    i = 0
                    for c in self.clients.keys():
                        if c==client:
                            break
                        i +=1
                    self.remove_user(client,i)
                    break
                    
            except:
                break
