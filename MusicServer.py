import pyaudio
import wave
from time import sleep
from threading import Thread
import Tkinter
import os
import random
from connection import SocketManager
from DataBase import DataBase

class MusicServer(object):
    def __init__(self):
        #creating my socket to connect with others
        self.server = SocketManager(3540)
        
        #creating the base for the gui
        self.root = Tkinter.Tk()

        #create the data base
        self.data = DataBase("DataBase.txt",self.root)
        
        self.currentSong = -1 #follow the index of the song
        self.newS = None #saving the location for new songs
        self.song = None #the song that currently is running  
        self.file = None #the file of the song
        self.keepGoing = True #controll the running system
        self.stop = False #stop or play the song
        self.rand = True

    def musicSender(self):
        l = 0 #false
        while self.keepGoing: #if the gui is still open
            if True in self.server.clients.values() and self.file!=None: #if there is someone connected
                if self.file.tell()<=self.file.getnframes(): #if thre is info and the song is not over
                        if not self.stop: #if the song is not on stop mode
                            l=self.file.readframes(16234) #read from the song file
                            self.server.broadcast(l)
                            sleep(0.333) 

        if self.file!=None:
            self.file.close()
        for clientSocket in self.server.clients: #disconnect from all the clients
            clientSocket.close()

    def musicChanger(self):
        while self.keepGoing: #if the gui is still open
            if None!=self.newS: #if there is new song being asked
                if self.newS!="": #to check it is not empty string
                    try:
                        if self.file!=None: #if its not the first song being played
                            self.file.close() #close the last song
                        self.file=wave.open(self.newS,'rb') #open the new song

                        #save the current song with the right syntax
                        temp = self.newS.split("\\")                        
                        temp = temp[len(temp)-1] 
                        temp = temp.split("/")
                        self.song = temp[len(temp)-1]
                        
                        self.newS = None
                    except:
                        print self.newS
                        #print "sorry, there is a problem"
            if True in self.server.clients.values():
                if self.file!=None: #if there is someone connected
                    if not self.stop and len(self.server.clients)>0 and self.file.tell()==self.file.getnframes(): #play random song if no song has been chosen
                        if self.rand:
                            self.chooseRandomSong() #activate random song if no song is being played
                        else:
                            self.chooseNextSong()
                else:
                    self.chooseNextSong()

    def chooseRandomSong(self):
        try:
            maybeSong = self.song #make sure the random song is not the last one
            while self.song==maybeSong: #make sure the random song is not the last one
                temp = random.choice(os.listdir(os.getcwd()+"\\songs")) #choose random file from the songs
                self.currentSong = os.listdir(os.getcwd()+"\\songs").index(temp)
                print temp
                print self.song
                if ".wav" in temp:
                    maybeSong=temp
            self.newS = "songs\\"+maybeSong #save the path to the song
        except:
            pass
            
    def chooseNextSong(self):
        self.otherSong(True)

    def changeSongTime(self): #move to time that needed when the button being pressed
        if self.file!= None: #if the restart button is being pressed
            self.file.setpos(0) #start over the song
        
    def otherSong(self,mode):
        try:
            if True in self.server.clients.values(): #if there is someone connected
                temp = os.listdir(os.getcwd()+"\\songs")
                if len(temp)>0:
                    if mode:
                        if len(temp)>self.currentSong+1:
                            self.currentSong+=1
                            s = temp[self.currentSong]
                        else:
                            s = temp[0]
                            self.currentSong=0
                    else:
                        if self.currentSong != 0:
                            self.currentSong-=1
                            s = temp[self.currentSong]
                        else:
                            s = temp[-1]
                            self.currentSong=len(temp)-1
                    print s     
                    if ".wav" in s:
                        self.newS = "songs\\"+s #save the path to the song
        except:
            pass
                    
    def newConnection(self): #while the app is working wait for new clients to join and add them
        while self.keepGoing:
            (clientSocket,clientAddress)=self.server.accept()
            self.server.clients[clientSocket] = False
            self.server.clientsAdresess.append(clientAddress)
            self.server.names[clientSocket]= None
            self.listen = Thread(target = self.server.listen_to_clients,
                                 args = (clientSocket,self.data,))
            self.listen.start()
            print "welcome " + str(clientAddress) + "\n"
