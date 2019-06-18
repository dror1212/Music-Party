import socket
import pyaudio
import wave
from time import sleep
from time import time
from threading import Thread
import Tkinter
import tkFileDialog as fb
import tkMessageBox
import os
import random
import tkFont
import pickle
import md5
from connection import SocketManager
from DataBase import DataBase
from MusicDownloader import musicDownloader
from recorder import Recorder
from MusicServer import MusicServer

class Server(MusicServer):
    def __init__(self):
        super(Server,self).__init__()

        #thread for repeatetly acceptong new connections
        self.new = Thread(target = self.newConnection)
        
        #thread for sending the data
        self.music = Thread(target = self.musicSender)
        self.change = Thread(target = self.musicChanger)
        self.update = Thread(target = self.updateData)
        
        self.record = Recorder(self.root)
        self.downloader = musicDownloader(self.root)
        
        #placing and creating the gui
        self.CreateTheControllBoared()

    def main(self):
        #thread for repeatetly acceptong new connections
        self.data.create()
        
        self.new.start()
        
        #thread for sending the data
        self.change.start()
        
        self.music.start()

        #needed to make the GUI work properly
        self.update.start()

        self.do()
        
    def do(self):
        while self.keepGoing:
            try: #update the gui data
                self.root.update_idletasks()
                self.root.update()
            except:
                break

    def updateData(self): #updating the data on the screen
        while self.keepGoing:
            try:
                last = self.timew.get()
                sleep(0.1)
                if self.file!=None:
                    #taking only the song name
                    name = self.song.split(".wav")[0]
                    try:
                        self.currentSongDisplay.config(text=name.upper())#showing the song name on the screen
                        self.currentSongDisplay.place(x=(800-self.currentSongDisplay.winfo_width())/2,y=5)
                    except:
                        pass
                    try:
                        self.timew.configure(to = self.file.getnframes()/self.file.getframerate(),
                                             tickinterval=self.file.getnframes()/self.file.getframerate())
                    except:
                        pass
                    try:
                        if last != self.timew.get():
                            if self.file.tell()/self.file.getframerate()>=1:
                                self.file.setpos(self.file.getframerate()*self.timew.get())
                        if self.timew.get()!=self.file.tell():
                            self.timew.set(self.file.tell()/self.file.getframerate())
                    except:
                        pass
            except:
                print "I want to know"
        
    def chooseNewSong(self,b): #open window to let the controller choose a new song
        temp = 9999
        temp = fb.askopenfilename(initialdir=os.getcwd()+"\\songs",title = "Select file",filetypes=[("Wave files", "*.wav")])
        while temp==9999:
            time.sleep(0.1)
        
        self.newS = temp
        if self.newS!="" and self.newS!=" " and self.newS!=None:
            try:
                self.currentSong = os.listdir(os.getcwd()+"\\songs").index(self.newS.split("/")[-1])
            except:
                pass

    def setPlayStatus(self,b): #when choosing new song put on playing mode
        b.config(text="Stop",bg="red3")
        self.stop = False

    def changeStatus(self,b): #stop/play the song when the button is being pressed
        if self.stop:
            b.config(text="Stop",bg="red3")
        else:
            b.config(text="Play",bg="lawn green")
        self.stop = not self.stop

    def randOrNot(self,b): #stop/play the song when the button is being pressed
        if self.rand:
            b.config(text="Random",bg="tomato2")
        else:
            b.config(text="Next",bg="sienna1")
        self.rand = not self.rand
                    
    def callback(self): #make sure the controller want to close the app
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.keepGoing=False; #make everything stop
            self.root.destroy() #close the gui

    def CreateTheControllBoared(self):
        #setting the title
        self.root.title("Music Party Controller")

        #setting the logo
        self.root.wm_iconbitmap('pictures\\head.ico')
        #setting the background color

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

        #Text for showing the current song
        self.currentSongDisplay = Tkinter.Label(self.root,text="No song",font="Arial 16 bold",fg="white",bg="black")
        #creating the buttons
        playOrStop = Tkinter.Button(self.root, text ="Stop",
                                    command = lambda: self.changeStatus(playOrStop),
                                    bg="red3",font = helv2)        

        randOrNext = Tkinter.Button(self.root, text ="Next", command = lambda: self.randOrNot(randOrNext),
                                    bg="sienna1",font = helv2)        

        nextSong = Tkinter.Button(self.root, text ="Forward", command = lambda: self.otherSong(True),bg="white",
                                  font = helv2)
        previosSong = Tkinter.Button(self.root, text ="Backward", command = lambda: self.otherSong(False),bg="white",
                                     font = helv2)
        
        timeReset = Tkinter.Button(self.root, text ="Restart The Song", command = lambda: self.changeSongTime(),
                                   bg="white",font = helv2)
        changeSong = Tkinter.Button(self.root, text ="Choose song", command = lambda: self.chooseNewSong(playOrStop),
                                    bg="white",font = helv36)
        register = Tkinter.Button(self.root, text ="Register", command = lambda: self.data.Page(),bg="white",
                                  font = helv2)
        download = Tkinter.Button(self.root, text ="Download New Song", command = lambda: self.downloader.Page(),
                                   bg="white",font = helv2)
        record = Tkinter.Button(self.root, text ="Record", command = lambda: self.record.Page(),
                                   bg="white",font = helv2)
        #setting the size of all the objects
        playOrStop.config(height=3, width = 20,relief=Tkinter.GROOVE)
        randOrNext.config(height=1, width = 8,relief=Tkinter.GROOVE)
        changeSong.config(height=2 , width = 15,relief=Tkinter.GROOVE)
        timeReset.config(height=3, width = 20,relief=Tkinter.GROOVE)
        nextSong.config(height=3, width = 20,relief=Tkinter.GROOVE)
        previosSong.config(height=3, width = 20,relief=Tkinter.GROOVE)
        register.config(height=3, width = 20,relief=Tkinter.GROOVE)
        download.config(height=3, width = 20,relief=Tkinter.GROOVE)
        record.config(height=3, width = 20,relief=Tkinter.GROOVE)

    
        #placing everything
        changeSong.place(x=308, y=50)
        playOrStop.place(x=315, y=290)
        randOrNext.place(x=362,y=120)
        timeReset.place(x=315, y=230)
        previosSong.place(x=145, y=230)
        nextSong.place(x=485, y=230)
        self.currentSongDisplay.place(x=0,y=0)
        register.place(x=315, y=350)
        download.place(x=315, y=410)
        record.place(x=315, y=470)

        self.timew = Tkinter.Scale(self.root, from_=0, to=0,tickinterval=10, orient=Tkinter.HORIZONTAL)
        self.timew.config(length = 600,width=20, fg = "white", bg = "black")
        self.timew.place(x = 97, y = 150)
