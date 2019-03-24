import socket
import pyaudio
import wave
import time
from threading import Thread
import Tkinter
import tkFileDialog as fb
import tkMessageBox
import os
import random
import tkFont

class Server():
    def __init__(self):

        #creating my socket to connect with others
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',3334))
        self.server.listen(10)

        #to save the info about my clients
        self.clients=[]
        self.clientsAdresess = []

        #thread for repeatetly acceptong new connections
        self.new = Thread(target = self.newConnection)
        #thread for sending the data
        self.music = Thread(target = self.musicSender)

        #creating the base for the gui
        self.root = Tkinter.Tk()

        #info I need to use in all the code
        self.newS = None #saving the location for new songs
        self.song = None #the song that currently is running       
        self.file = None #the file of the song
        self.keepGoing = True #controll the running system
        self.stop = False #stop or play the song
        #placing and creating the gui
        self.CreateTheControllBoared()
        
    def main(self):
        #thread for repeatetly acceptong new connections
        self.new.start()
        
        #thread for sending the data
        self.music.start()

        #needed to make the GUI work properly
        self.root.mainloop()
        
    def musicSender(self):
        l = 0 #false
        while self.keepGoing: #if the gui is still open
            self.updateData() #updating the data about the songs that shown
            if None!=self.newS: #if there is new song being asked
                if self.newS!="": #to check it is not empty string
                    try:
                        if self.file!=None: #if its not the first song being played
                            self.file.close() #close the last song
                        self.file=wave.open(self.newS,'rb') #open the new song
                        l=self.file.readframes(16) #read from the new song
                        self.song = self.newS #save the current song
                        self.newS = None
                    except:
                        print "sorry, there is a problem"
            if len(self.clients)>0: #if there is someone connected
                if l and self.file.tell()<=self.file.getnframes(): #if thre is info and the song is not over
                    try:                        
                        if not self.stop: #if the song is not on stop mode
                            l=self.file.readframes(16) #read from the song file
                            temp = self.clients #to prevent problems
                            counter = 0
                            for clientSocket in temp: #send to all the clients the music
                                try:
                                    clientSocket.send(l)
                                except: #if one of the clients is not connected anymore delete it
                                    print "good bye " + str(self.clientsAdresess[counter])
                                    del self.clients[counter]
                                    del self.clientsAdresess[counter]
                                counter = counter+1
                    except:
                        pass
                elif not self.stop and len(self.clients)>0: #play random song if no song has been chosen
                    maybeSong = self.song #make sure the random song is not the last one
                    while self.song==maybeSong: #make sure the random song is not the last one
                        temp = random.choice(os.listdir(os.getcwd()+"\\songs")) #choose random file from the songs
                        if ".wav" in temp:
                            maybeSong=temp
                    self.newS = "songs\\"+maybeSong #save the path to the song
                    
        if self.file!=None:
            self.file.close()
        for clientSocket in self.clients: #disconnect from all the clients
            clientSocket.send("ServerSentToClient")
            clientSocket.close()
            
    def newConnection(self): #while the app is working wait for new clients to join and add them
        while self.keepGoing:
            (clientSocket,clientAddress)=self.server.accept()
            self.clients.append(clientSocket)
            self.clientsAdresess.append(clientAddress)            
            print "welcome " + str(clientAddress) + "\n"
            
    def updateData(self): #updating the data on the screen
        if not self.stop:
            if self.file!=None:
                #taking only the song name
                temp = self.song.split("\\")
                name = temp[len(temp)-1]
                temp = name.split("/")
                name = temp[len(temp)-1]
                name = name.split(".")[0]
                self.currentSongDisplay.config(text=str(name.upper()))#showing the song name on the screen
                time = (self.file.getnframes() - self.file.tell())/self.file.getframerate()
                minutes = time /60
                seconds = time % 60
                if seconds<10:
                    seconds = "0" + str(seconds)
                if minutes<10:
                    minutes = "0" + str(minutes)
                time = str(minutes) + ":" + str(seconds)
                self.TimeLeft.configure(text=time) #showing how much time is left fot the song
            else:
                self.TimeLeft.configure(text="0")

    def chooseNewSong(self,b): #open window to let the controller choose a new song
        self.newS = fb.askopenfilename(initialdir=os.getcwd()+"\\songs",title = "Select file",filetypes=[("Wave files", "*.wav")])
        self.setPlayStatus(b) #when choosing new song put on playing mode

    def setPlayStatus(self,b): #when choosing new song put on playing mode
        b.config(text="Stop",bg="red3")
        self.stop = False
    
    def changeStatus(self,b): #stop/play the song when the button is being pressed
        if self.stop:
            b.config(text="Stop",bg="red3")
        else:
            b.config(text="Play",bg="lawn green")
        self.stop = not self.stop
        
            
    def changeSongTime(self,check,e): #move to time that needed when the button being pressed
        if check==None and self.file!= None: #if the restart button is being pressed
            self.file.setpos(0) #start over the song
        elif self.file!= None and e!=None and e.get()!="": #check if there is a reason
            x = int(e.get())
            if check: #if forward is being pressed
                if (self.file.getnframes() - self.file.tell())/self.file.getframerate() > x: 
                    self.file.setpos(self.file.tell() + self.file.getframerate()*x)
                else:
                    self.file.setpos(self.file.getframes())
            else: #if backward is being pressed
                if self.file.tell()/self.file.getframerate()>x:
                    self.file.setpos(self.file.tell() - self.file.getframerate()*x)
                else:
                    self.file.setpos(0)
                    
    def callback(self): #make sure the controller want to close the app
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.keepGoing=False; #make everything stop
            self.root.destroy() #close the gui
            
    def CheckIfNumber(self, P): #check if what pressed on the keybored is number
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
            
    def CreateTheControllBoared(self):
        #setting the title
        self.root.title("Music Party Controller")

        #setting the logo
        self.root.wm_iconbitmap('pictures\\head.ico')

        #setting the background color
        self.root.config(bg="DarkOrange3")

        #setting the size of the controller
        self.root.geometry("800x550")
        self.root.resizable(0, 0)

        #ask if they want to quit for sure when X is clicked
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        #creating the background picture
        photo = Tkinter.PhotoImage(file="pictures\\b.gif")
        w = Tkinter.Label(self.root, image=photo)
        w.photo = photo
        w.pack()

        #fonts
        helv36 = tkFont.Font(family='Helvetica', size=15, weight='bold')
        helv2 = tkFont.Font(family='Helvetica', size=10, weight='bold')
        large_font = ('Verdana',25)

        #command for checking the data goun into the entry
        vcmd = (self.root.register(self.CheckIfNumber))

        #creating the entry
        e = Tkinter.Entry(self.root,font=large_font,justify='center', validate='all', validatecommand=(vcmd, '%P'))

        #Text for showing the current song
        self.currentSongDisplay = Tkinter.Label(self.root,text="No song",font="Times 20",fg="white",bg="black")
        self.TimeLeft = Tkinter.Label(self.root,text="0",font="Times 20",fg="white",bg="black")        
        #creating the buttons
        playOrStop = Tkinter.Button(self.root, text ="Stop", command = lambda: self.changeStatus(playOrStop),bg="red3",font = helv2)        
        timeChangeF = Tkinter.Button(self.root, text ="Forward", command = lambda: self.changeSongTime(True,e),bg="white",font = helv2)
        timeChangeB = Tkinter.Button(self.root, text ="Backward", command = lambda: self.changeSongTime(False,e),bg="white",font = helv2)
        timeReset = Tkinter.Button(self.root, text ="Restart The Song", command = lambda: self.changeSongTime(None,e),bg="white",font = helv2)
        changeSong = Tkinter.Button(self.root, text ="Choose song", command = lambda: self.chooseNewSong(playOrStop),bg="white",font = helv36)

        #setting the size of all the objects
        playOrStop.config(height=3, width = 20)
        changeSong.config(height=2 , width = 15)
        timeReset.config(height=3, width = 20)
        timeChangeB.config(height=3, width = 20)
        timeChangeF.config(height=3, width = 20)
    
        #placing everything
        changeSong.place(x=308, y=80)
        e.place(x=187, y=180)
        playOrStop.place(x=315, y=320)
        timeReset.place(x=315, y=260)
        timeChangeB.place(x=145, y=260)
        timeChangeF.place(x=485, y=260)
        self.currentSongDisplay.place(x=0,y=0)
        self.TimeLeft.place(x=0,y=30)
        
if __name__ == "__main__":
    music_party = Server() 
    music_party.main() #start everything
    os._exit(1)
