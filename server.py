import socket
import pyaudio
import wave
import time
from threading import Thread

class Server():
    def __init__(self):
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',3334))
        self.clients=[]
        self.clientsAdresess = []
        self.new = Thread(target = self.newConnection)
        self.newSong = Thread(target = self.newSong)
        self.server.listen(10)
        self.newS = None

    def main(self):
        self.new.start()
        self.newSong.start()
        
        time.sleep(1)
        f = None

        l = 0
        while True:
            if None!=self.newS:
                if f != None:
                    f.close()
                f=open(self.newS + ".wav",'rb')
                l=f.read(2048)
                self.newS = None
            if len(self.clients)>0 and l:
                l=f.read(2048)
                if l:
                    temp = self.clients
                    counter = 0
                    for clientSocket in temp:
                        try:
                            clientSocket.send(l)
                        except:
                            del self.clients[counter]
                            del self.clientsAdresess[counter]
                        counter = counter+1

        f.close()
        clientSocket.send("ServerSentToClient")

    def newConnection(self):
        while True: 
            (clientSocket,clientAddress)=self.server.accept()
            self.clients.append(clientSocket)
            self.clientsAdresess.append(clientAddress)            
            print "welcome \n"
            
    def newSong(self):
        while True:
            if len(self.clients)>0:
                x = raw_input("what song do you want to hear?")
                x = x.lower()
                self.newS = x
        

x = Server()
x.main()
