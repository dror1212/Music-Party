import socket
import pyaudio
import wave
import time
from threading import Thread
import Tkinter
import tkFileDialog as fb
import tkMessageBox
import os


class Server():
    def __init__(self):
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',5438))
        self.clients=[]
        self.clientsAdresess = []
        self.new = Thread(target = self.newConnection)
        self.music = Thread(target = self.musicSender)
        self.server.listen(10)
        self.newS = None
        self.root = Tkinter.Tk()
        self.root.title("Music Party Controller")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.wm_iconbitmap('head.ico')
        self.file = None
        self.keepGoing = True
        
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
                        self.file=wave.open(self.newS,'rb')
                        l=self.file.readframes(2048)
                    except:
                        print ", this song does not exist"
                self.newS = None
            if len(self.clients)>0 and l:
                try:
                    l=self.file.readframes(2048)
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
            print "welcome \n"
            
    def chooseNewSong(self):
        self.newS = fb.askopenfilename(title = "Select file",filetypes=[("Wave files", "*.wav")])

    def changeSongTime(self,sec,check,e):
        try:
            x = int(sec)
            if self.file!= None:
                if check:
                    self.file.setpos(self.file.tell() + self.file.getframerate()*x)
                else:
                    if self.file.tell()/self.file.getframerate()>x:
                        self.file.setpos(self.file.tell() - self.file.getframerate()*x)
                    else:
                        self.file.setpos(0)
        except:
            while len(e.get())>0:
                e.delete(len(e.get())-1)
                
    def callback(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.keepGoing=False;
            self.root.destroy()
            
    def newSong(self):
        changeSong = Tkinter.Button(self.root, text ="Choose song", command = self.chooseNewSong)
        changeSong.pack()
        e = Tkinter.Entry(self.root)
        e.pack()
        timeChangeF = Tkinter.Button(self.root, text ="Forward", command = lambda: self.changeSongTime(e.get(),True,e))
        timeChangeB = Tkinter.Button(self.root, text ="Backward", command = lambda: self.changeSongTime(e.get(),False,e))
        timeReset = Tkinter.Button(self.root, text ="Restart The Song", command = lambda: self.changeSongTime("99999",False,e))
        timeReset.pack()
        timeChangeF.pack()
        timeChangeB.pack()
        self.root.mainloop()
        
if __name__ == "__main__":
    x = Server()
    x.main()
    os._exit(1)
