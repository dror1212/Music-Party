import socket
import pyaudio
import wave
import time
from threading import Thread

class Server():
    def __init__(self):
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',3536))
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
                if f!= None and self.newS=="10":
                    f.setpos(f.tell() + f.getframerate()*10)
                    time.sleep(0.5)
                elif f!= None and self.newS=="-10":
                    if f.tell()/f.getframerate()>10:
                        f.setpos(f.tell() - f.getframerate()*10)
                    else:
                        f.setpos(0)
                    time.sleep(0.5)
                else:
                    try:
                        f=wave.open(self.newS + ".wav",'rb')
                        l=f.readframes(2048)
                    except:
                        print ", this song does not exist"
                self.newS = None
            if len(self.clients)>0 and l:
                try:
                    l=f.readframes(2048)
                    temp = self.clients
                    counter = 0
                    for clientSocket in temp:
                        try:
                            clientSocket.send(l)
                        except:
                            del self.clients[counter]
                            del self.clientsAdresess[counter]
                        counter = counter+1
                except:
                    pass

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
