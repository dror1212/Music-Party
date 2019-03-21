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
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',5538))
        self.clients=[]
        self.clientsAdresess = []
        
        self.new = Thread(target = self.newConnection)
        self.music = Thread(target = self.musicSender)
        
        self.server.listen(10)
        
        self.newS = None
        self.song = None
        
        self.root = Tkinter.Tk()
        self.root.title("Music Party Controller")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.wm_iconbitmap('pictures\\head.ico')
        self.root.config(bg="DarkOrange3")
        self.root.geometry("800x550")
        self.root.resizable(0, 0)
        
        photo = Tkinter.PhotoImage(file="pictures\\b.gif")
        self.w = Tkinter.Label(self.root, image=photo)
        self.w.photo = photo
        self.w.pack()
        self.file = None
        self.keepGoing = True
        self.stop = False
        
        
    def main(self):
        self.new.start()
        self.music.start()
        self.newSong()

    def musicSender(self):
        l = 0
        while self.keepGoing:
            if None!=self.newS:
                if self.newS!="":
                    try:
                        if self.file!=None:
                            self.file.close()
                        self.file=wave.open(self.newS,'rb')
                        l=self.file.readframes(2048)
                        self.song = self.newS
                        self.newS = None
                        self.stop=False
                    except:
                        print "sorry, there is a problem"
            if len(self.clients)>0:
                if l and self.file.tell()<=self.file.getnframes():
                    #try:
                        if not self.stop:
                            l=self.file.readframes(2048)
                            temp = self.clients
                            counter = 0
                            for clientSocket in temp:
                                try:
                                    clientSocket.send(l)
                                except:
                                    print "good bye " + str(self.clientsAdresess[counter])
                                    del self.clients[counter]
                                    del self.clientsAdresess[counter]
                                counter = counter+1
                    #except:
                elif not self.stop and len(self.clients)>0: #play random song
                    maybeSong = self.song
                    while self.song==maybeSong:
                        temp = random.choice(os.listdir(os.getcwd()+"\\songs"))
                        if ".wav" in temp:
                            maybeSong=temp
                    self.newS = "songs\\"+maybeSong
                    
        if self.file!=None:
            self.file.close()
        for clientSocket in self.clients:
            clientSocket.send("ServerSentToClient")
            clientSocket.close()
            
    def newConnection(self):
        while self.keepGoing:
            (clientSocket,clientAddress)=self.server.accept()
            self.clients.append(clientSocket)
            self.clientsAdresess.append(clientAddress)            
            print "welcome " + str(clientAddress) + "\n"
            
    def chooseNewSong(self):
        self.newS = fb.askopenfilename(initialdir=os.getcwd()+"\\songs",title = "Select file",filetypes=[("Wave files", "*.wav")])
    def stopGoing(self):
        self.stop = True
        
    def Going(self):
        self.stop = False
        
    def changeSongTime(self,check,e):
        if check==None and self.file!= None:
            self.file.setpos(0)
        elif self.file!= None and e!=None and e.get()!="":
            x = int(e.get())
            if check:
                if (self.file.getnframes() - self.file.tell())/self.file.getframerate() > x:
                    self.file.setpos(self.file.tell() + self.file.getframerate()*x)
                else:
                    self.file.setpos(self.file.getnframes())
            else:
                if self.file.tell()/self.file.getframerate()>x:
                    self.file.setpos(self.file.tell() - self.file.getframerate()*x)
                else:
                    self.file.setpos(0)
                    
    def callback(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.keepGoing=False;
            self.root.destroy()
            
    def CheckIfNumber(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
            
    def newSong(self):
        helv36 = tkFont.Font(family='Helvetica', size=15, weight='bold')
        helv2 = tkFont.Font(family='Helvetica', size=10, weight='bold')
        changeSong = Tkinter.Button(self.root, text ="Choose song", command = self.chooseNewSong,bg="light goldenrod",font = helv36)
        changeSong.config(height=2 , width = 15)
        changeSong.place(x=308, y=5)

        vcmd = (self.root.register(self.CheckIfNumber))
        
        large_font = ('Verdana',25)
        e = Tkinter.Entry(self.root,font=large_font,justify='center', validate='all', validatecommand=(vcmd, '%P'))

        stopTheSong = Tkinter.Button(self.root, text ="Stop", command = lambda: self.stopGoing(),bg="wheat1",font = helv2)
        playTheSong = Tkinter.Button(self.root, text ="Play", command = lambda: self.Going(),bg="wheat1",font = helv2)
        stopTheSong.config(height=3, width = 20)
        playTheSong.config(height=3, width = 20)
        
        timeChangeF = Tkinter.Button(self.root, text ="Forward", command = lambda: self.changeSongTime(True,e),bg="tomato",font = helv2)
        timeChangeB = Tkinter.Button(self.root, text ="Backward", command = lambda: self.changeSongTime(False,e),bg="tomato",font = helv2)
        timeReset = Tkinter.Button(self.root, text ="Restart The Song", command = lambda: self.changeSongTime(None,e),bg="tomato",font = helv2)
        timeReset.config(height=3, width = 20)
        timeChangeB.config(height=3, width = 20)
        timeChangeF.config(height=3, width = 20)
        e.place(x=187, y=100)
        stopTheSong.place(x=478, y=287)
        playTheSong.place(x=156, y=287)
        timeReset.place(x=315, y=150)
        timeChangeB.place(x=145, y=150)
        timeChangeF.place(x=485, y=150)
        self.root.mainloop()
        
if __name__ == "__main__":
    x = Server()
    x.main()
    os._exit(1)
