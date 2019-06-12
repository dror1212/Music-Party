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

class Server():
    def __init__(self):

        #creating my socket to connect with others
        self.server = SocketManager(3540)

        self.data = DataBase("DataBase.txt")
        #thread for repeatetly acceptong new connections
        self.new = Thread(target = self.newConnection)
        #thread for sending the data
        self.music = Thread(target = self.musicSender2)

        self.change = Thread(target = self.musicChanger)

        self.update = Thread(target = self.updateData)

        #creating the base for the gui
        self.root = Tkinter.Tk()
        self.register_screen = None

        self.currentSong = -1 ####################
        
        #info I need to use in all the code
        self.newS = None #saving the location for new songs
        self.song = None #the song that currently is running       
        self.file = None #the file of the song
        self.keepGoing = True #controll the running system
        self.stop = False #stop or play the song
        #placing and creating the gui
        self.CreateTheControllBoared()

        self.rand = True

        self.t = None
        
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
    def musicSender2(self):
        l = 0 #false
        while self.keepGoing: #if the gui is still open
            if True in self.server.clients.values() and self.file!=None: #if there is someone connected
                if self.file.tell()<=self.file.getnframes(): #if thre is info and the song is not over
                        if not self.stop: #if the song is not on stop mode
                            l=self.file.readframes(32468) #read from the song file
                            self.server.broadcast(l)
                            sleep(0.732) 

        if self.file!=None:
            self.file.close()
        for clientSocket in self.server.clients: #disconnect from all the clients
            clientSocket.close()

    def musicSender(self):
        l = 0 #false
        while self.keepGoing: #if the gui is still open
            if True in self.server.clients.values() and self.file!=None: #if there is someone connected
                if self.file.tell()<=self.file.getnframes(): #if thre is info and the song is not over
                        if not self.stop: #if the song is not on stop mode
                            l=self.file.readframes(4) #read from the song file
                            self.server.broadcast(l)  

        if self.file!=None:
            self.file.close()
        for clientSocket in self.server.clients: #disconnect from all the clients
            clientSocket.close()
            
    def musicChanger(self):
        while self.keepGoing: #if the gui is still open
            if None!=self.newS: #if there is new song being asked
                if self.newS!="": #to check it is not empty string
                    print "rrr"
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
                        print "sorry, there is a problem"
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
            maybeSong = self.song #make sure the random song is not the last one
            while self.song==maybeSong: #make sure the random song is not the last one
                temp = random.choice(os.listdir(os.getcwd()+"\\songs")) #choose random file from the songs
                self.currentSong = os.listdir(os.getcwd()+"\\songs").index(temp)
                print temp
                print self.song
                if ".wav" in temp:
                    maybeSong=temp
            self.newS = "songs\\"+maybeSong #save the path to the song

    def chooseNextSong(self):
        self.otherSong(True)
           
    def updateData(self): #updating the data on the screen
        while self.keepGoing:
            try:
                last = self.timew.get()
                sleep(0.1)
                if self.file!=None:
                    #taking only the song name
                    name = self.song.split(".wav")[0]
                    try:
                        self.currentSongDisplay.config(text=str(name.upper()))#showing the song name on the screen
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
        if self.newS!="" and self.newS!=" ":
            self.currentSong = os.listdir(os.getcwd()+"\\songs").index(self.newS.split("/")[-1])
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

    def randOrNot(self,b): #stop/play the song when the button is being pressed
        if self.rand:
            b.config(text="Random",bg="tomato2")
        else:
            b.config(text="Next",bg="sienna1")
        self.rand = not self.rand
        

    def otherSong(self,mode):
        temp = os.listdir(os.getcwd()+"\\songs")
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
                
        if ".wav" in s:
            self.newS = "songs\\"+s #save the path to the song
                
    def changeSongTime(self): #move to time that needed when the button being pressed
        if self.file!= None: #if the restart button is being pressed
            self.file.setpos(0) #start over the song
                    
    def callback(self): #make sure the controller want to close the app
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.keepGoing=False; #make everything stop
            self.root.destroy() #close the gui
            
    def CheckIfNumber(self, P): #check if what pressed on the keybored is number
        try:
            if str.isdigit(P) or P=="":
                return True
            else:
                return False
        except:
            return False
        
    def res(self):
        self.register_screen.destroy()
        self.register_screen = None
        
    def registerationPage(self):
        if self.register_screen == None:
            self.register_screen = Tkinter.Toplevel(self.root)
            self.register_screen.title("Register")
            self.register_screen.geometry("300x250")
            self.register_screen.wm_iconbitmap('pictures\\head.ico')
            self.register_screen.protocol("WM_DELETE_WINDOW", self.res)
            self.register_screen.resizable(0, 0)
            username = Tkinter.StringVar()
            password = Tkinter.StringVar()
     
            self.msg = Tkinter.Label(self.register_screen, text="Please enter details below", bg="grey")
            self.msg.pack()
            Tkinter.Label(self.register_screen, text="").pack()
            username_lable = Tkinter.Label(self.register_screen, text="Username * ")
            username_lable.pack()
            self.username_entry = Tkinter.Entry(self.register_screen, textvariable=username)
            self.username_entry.pack()
            password_lable = Tkinter.Label(self.register_screen, text="Password * ")
            password_lable.pack()
            self.password_entry = Tkinter.Entry(self.register_screen, textvariable=password, show='*')
            self.password_entry.pack()
            Tkinter.Label(self.register_screen, text="").pack()
            Tkinter.Button(self.register_screen, text="Register", width=10, height=1, bg="grey", command = lambda: self.register_user(username.get(),password.get())).pack()
            self.username_entry.focus_set()
            
    def register_user(self,username,password):
        b = self.data.get()

        check = self.data.check_register(username,password)
        self.msg.config(text=check)
                
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()
        
    def CreateTheControllBoared(self):
        #setting the title
        self.root.title("Music Party Controller")

        #setting the logo
        self.root.wm_iconbitmap('pictures\\head.ico')
        #setting the background color
        #self.root.config(bg="DarkOrange3")

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

        #Text for showing the current song
        self.currentSongDisplay = Tkinter.Label(self.root,text="No song",font="Arial 24 bold",fg="white",bg="black")
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
        register = Tkinter.Button(self.root, text ="Register", command = lambda: self.registerationPage(),bg="white",
                                  font = helv2)

        #setting the size of all the objects
        playOrStop.config(height=3, width = 20,relief=Tkinter.GROOVE)
        randOrNext.config(height=1, width = 8,relief=Tkinter.GROOVE)
        changeSong.config(height=2 , width = 15,relief=Tkinter.GROOVE)
        timeReset.config(height=3, width = 20,relief=Tkinter.GROOVE)
        nextSong.config(height=3, width = 20,relief=Tkinter.GROOVE)
        previosSong.config(height=3, width = 20,relief=Tkinter.GROOVE)
        register.config(height=3, width = 20,relief=Tkinter.GROOVE)
    
        #placing everything
        changeSong.place(x=308, y=80)
        playOrStop.place(x=315, y=320)
        randOrNext.place(x=362,y=150)
        timeReset.place(x=315, y=260)
        previosSong.place(x=145, y=260)
        nextSong.place(x=485, y=260)
        self.currentSongDisplay.place(x=0,y=0)
        register.place(x=315, y=380)

        self.timew = Tkinter.Scale(self.root, from_=0, to=0,tickinterval=10, orient=Tkinter.HORIZONTAL)
        self.timew.config(length = 600,width=20, fg = "white", bg = "black")
        self.timew.place(x = 97, y = 180)
