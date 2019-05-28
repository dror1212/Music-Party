import socket

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
        
