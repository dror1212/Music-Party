import socket
import pyaudio
import wave
from time import sleep
from threading import Thread
import Tkinter
import tkFileDialog as fb
import tkMessageBox
import os
import random
import tkFont
import pickle
import md5

class Server():
    def __init__(self):

        #creating my socket to connect with others
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',3539))
        self.server.listen(10)

        #to save the info about my clients
        self.clients = {}
        self.names = {}
        self.clientsAdresess = []
        #thread for repeatetly acceptong new connections
        self.new = Thread(target = self.newConnection)
        #thread for sending the data
        self.music = Thread(target = self.musicSender)

        self.update = Thread(target = self.updateData)

        #creating the base for the gui
        self.root = Tkinter.Tk()
        self.register_screen = None

        self.currentSong = 0 ####################
        
        #info I need to use in all the code
        self.newS = None #saving the location for new songs
        self.song = None #the song that currently is running       
        self.file = None #the file of the song
        self.keepGoing = True #controll the running system
        self.stop = False #stop or play the song
        #placing and creating the gui
        self.CreateTheControllBoared()

        self.rand = True
        
    def main(self):
        #thread for repeatetly acceptong new connections
        self.new.start()
        
        #thread for sending the data
        self.music.start()

        self.update.start()
        
        #needed to make the GUI work properly
        self.do()
        
    def do(self):
        while self.keepGoing:
            try:
                self.root.update_idletasks()
                self.root.update()
            except:
                break
            
    def musicSender(self):
        l = 0 #false
        while self.keepGoing: #if the gui is still open
            if None!=self.newS: #if there is new song being asked
                if self.newS!="": #to check it is not empty string
                    try:
                        if self.file!=None: #if its not the first song being played
                            self.file.close() #close the last song
                        self.file=wave.open(self.newS,'rb') #open the new song
                        l=self.file.readframes(32) #read from the new song

                        #save the current song with the right syntax
                        temp = self.newS.split("\\")                        
                        temp = temp[len(temp)-1] 
                        temp = temp.split("/")
                        self.song = temp[len(temp)-1]
                        
                        self.newS = None
                    except:
                        print "sorry, there is a problem"
            if True in self.clients.values(): #if there is someone connected
                if l and self.file.tell()<=self.file.getnframes(): #if thre is info and the song is not over
                    try:                        
                        if not self.stop: #if the song is not on stop mode
                            l=self.file.readframes(32) #read from the song file
                            temp = self.clients #to prevent problems
                            counter = 0
                            for clientSocket in temp.keys(): #send to all the clients the music
                                try:
                                    if temp[clientSocket]:
                                        clientSocket.send(l)
                                except: #if one of the clients is not connected anymore delete it
                                    print "good bye " + str(self.clientsAdresess[counter])
                                    del self.clients[clientSocket]
                                    del self.names[clientSocket]
                                    del self.clientsAdresess[counter]
                                counter = counter+1
                    except:
                        print "sorry, there is a problem 2"
                elif not self.stop and len(self.clients)>0: #play random song if no song has been chosen
                    if self.rand:
                        self.chooseRandomSong() #activate random song if no song is being played
                    else:
                        self.chooseNextSong()
                        

        if self.file!=None:
            self.file.close()
        for clientSocket in self.clients: #disconnect from all the clients
            clientSocket.send("ServerSentToClient")
            clientSocket.close()

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
        
    def newConnection(self): #while the app is working wait for new clients to join and add them
        while self.keepGoing:
            (clientSocket,clientAddress)=self.server.accept()
            self.clients[clientSocket] = True
            self.clientsAdresess.append(clientAddress)
            self.names[clientSocket]= None
            #self.listen = Thread(target = self.listen_to_clients, args = (clientSocket,))
            #self.listen.start()
            print "welcome " + str(clientAddress) + "\n"
         
    def updateData(self): #updating the data on the screen
        while self.keepGoing:
            try:
                last = self.timew.get()
                sleep(0.5)
                if self.file!=None:
                    #taking only the song name
                    name = self.song.split(".wav")[0]
                    try:
                        self.currentSongDisplay.config(text=str(name.upper()))#showing the song name on the screen
                        self.currentSongDisplay.place(x=(800-self.currentSongDisplay.winfo_width())/2,y=5)
                    except:
                        pass
                    try:
                        self.timew.configure(to = self.file.getnframes()/self.file.getframerate(),tickinterval=self.file.getnframes()/self.file.getframerate())
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
                    
                    #time = (self.file.getnframes() - self.file.tell())/self.file.getframerate()
                    #minutes = time /60
                    #seconds = time % 60
                    #if seconds<10:
                        #seconds = "0" + str(seconds)
                    #if minutes<10:
                        #minutes = "0" + str(minutes)
                    #time = str(minutes) + ":" + str(seconds)
                    #self.TimeLeft.configure(text=time) #showing how much time is left fot the song
                #else:
                    #self.TimeLeft.configure(text="0")
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

    def listen_to_clients(self,client):
        try:
            with open('DataBase.txt', 'rb') as data_base:
                b = pickle.load(data_base)
        except:
            with open("DataBase.txt", 'wb') as data_base:
                pickle.dump({}, data_base, protocol=pickle.HIGHEST_PROTOCOL)
            with open('DataBase.txt', 'rb') as data_base:
                b = pickle.load(data_base)
        while True:
            try:
                x = client.recv(32)
                print x
                if "Connection:" in x:                    
                    with open('DataBase.txt', 'rb') as data_base:
                        b = pickle.load(data_base)
                    x = x.split(":")
                    x = x[-1].split(",")                    
                    name = x[0]
                    password = x[-1]
                    if name in b.keys():
                        if name in self.names.values():
                            client.send("This user is taken")
                        elif b[name]==md5.new(password).hexdigest():
                            self.clients[client]=True
                            self.names[client]=name
                            client.send("Connection accepted")
                        else:
                            client.send("Wrong password")
                    else:
                        client.send("This username does not exist")
                elif "Disconnect:" in x:
                    i = 0
                    for c in self.clients.keys():
                        if c==client:
                            break
                        i +=1
                    print "good bye " + str(self.clientsAdresess[i])
                    del self.clientsAdresess[i]
                    del self.clients[client]
                    del self.names[client]
                    break
                    
            except:
                break

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
                
    def changeSongTime(self,check,e): #move to time that needed when the button being pressed
        if check==None and self.file!= None: #if the restart button is being pressed
            self.file.setpos(0) #start over the song
        elif self.file!= None and e!=None and e.get()!="": #check if there is a reason
            x = int(e.get())
            if check: #if forward is being pressed
                if (self.file.getnframes() - self.file.tell())/self.file.getframerate() > x: 
                    self.file.setpos(self.file.tell() + self.file.getframerate()*x)
                else:
                    self.file.setpos(self.file.getnframes())
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
        try:
            with open('DataBase.txt', 'rb') as data_base:
                b = pickle.load(data_base)
        except:
            with open("DataBase.txt", 'wb') as data_base:
                pickle.dump({}, data_base, protocol=pickle.HIGHEST_PROTOCOL)
            with open('DataBase.txt', 'rb') as data_base:
                b = pickle.load(data_base)
        if username in b.keys():
            self.msg.config(text="The username " + username + " already exists")
        else:
            if not username.isspace() and not password.isspace() and username!="" and password!="":
                b[username] = md5.new(password).hexdigest()
                print b[username]
                self.msg.config(text="Username " + username + " was created succesfully")
                with open("DataBase.txt", 'wb') as data_base:
                    pickle.dump(b, data_base, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                self.msg.config(text="You can't leave any tab empty")
                
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()
        data_base.close()
        
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

        #creating the entry
        #e = Tkinter.Entry(self.root,font=large_font,justify='center', validate='all', validatecommand=(vcmd, '%P'))

        #Text for showing the current song
        self.currentSongDisplay = Tkinter.Label(self.root,text="No song",font="Arial 24 bold",fg="white",bg="black")
        #self.TimeLeft = Tkinter.Label(self.root,text="0",font="Times 20",fg="white",bg="black")        
        #creating the buttons
        playOrStop = Tkinter.Button(self.root, text ="Stop", command = lambda: self.changeStatus(playOrStop),bg="red3",font = helv2)        
        #timeChangeF = Tkinter.Button(self.root, text ="Forward", command = lambda: self.changeSongTime(True,e),bg="white",font = helv2)
        #timeChangeB = Tkinter.Button(self.root, text ="Backward", command = lambda: self.changeSongTime(False,e),bg="white",font = helv2)
        randOrNext = Tkinter.Button(self.root, text ="Next", command = lambda: self.randOrNot(randOrNext),bg="sienna1",font = helv2)        

        nextSong = Tkinter.Button(self.root, text ="Forward", command = lambda: self.otherSong(True),bg="white",font = helv2)
        previosSong = Tkinter.Button(self.root, text ="Backward", command = lambda: self.otherSong(False),bg="white",font = helv2)
        
        timeReset = Tkinter.Button(self.root, text ="Restart The Song", command = lambda: self.changeSongTime(None,None),bg="white",font = helv2)
        changeSong = Tkinter.Button(self.root, text ="Choose song", command = lambda: self.chooseNewSong(playOrStop),bg="white",font = helv36)
        register = Tkinter.Button(self.root, text ="Register", command = lambda: self.registerationPage(),bg="white",font = helv2)

        #setting the size of all the objects
        playOrStop.config(height=3, width = 20,relief=Tkinter.GROOVE)
        randOrNext.config(height=1, width = 8,relief=Tkinter.GROOVE)
        changeSong.config(height=2 , width = 15,relief=Tkinter.GROOVE)
        timeReset.config(height=3, width = 20,relief=Tkinter.GROOVE)
        #timeChangeB.config(height=3, width = 20,relief=Tkinter.GROOVE)
        #timeChangeF.config(height=3, width = 20,relief=Tkinter.GROOVE)
        nextSong.config(height=3, width = 20,relief=Tkinter.GROOVE)
        previosSong.config(height=3, width = 20,relief=Tkinter.GROOVE)
        register.config(height=3, width = 20,relief=Tkinter.GROOVE)
    
        #placing everything
        changeSong.place(x=308, y=80)
        #e.place(x=187, y=180)
        playOrStop.place(x=315, y=320)
        randOrNext.place(x=362,y=150)
        timeReset.place(x=315, y=260)
        #timeChangeB.place(x=145, y=260)
        #timeChangeF.place(x=485, y=260)
        previosSong.place(x=145, y=260)
        nextSong.place(x=485, y=260)
        self.currentSongDisplay.place(x=0,y=0)
        #self.TimeLeft.place(x=0,y=30)
        register.place(x=315, y=380)

        self.timew = Tkinter.Scale(self.root, from_=0, to=0,tickinterval=10, orient=Tkinter.HORIZONTAL)
        self.timew.config(length = 600,width=20, fg = "white", bg = "black")
        self.timew.place(x = 97, y = 180)
