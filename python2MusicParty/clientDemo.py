import socket
import time
import pyaudio
import Tkinter
from threading import Thread
from time import sleep
import os

class Client():
    def __init__(self):
        self.login_screen = Tkinter.Tk() #create the tkinter base
        
        #constans for the stream
        self.FORMAT=pyaudio.paInt16
        self.FSAMP = 48000

        self.p = pyaudio.PyAudio()
        self.clientSocket=socket.socket()

        self.tryToConnect()
        while True: #try to connect to ip untill it works
            self.ip = None
            self.waitForIp()
            try:
                self.msg.config(text = "Trying to connect")
                self.login_screen.update_idletasks()
                self.login_screen.update()
                self.clientSocket.connect((self.ip,3540))
                break
            except:
                self.msg.config(text = "Try again, wrong IP")

        self.login_screen.destroy()
        self.login_screen = Tkinter.Tk()
        
        self.stream = self.p.open(format=self.FORMAT,
                            channels=2,
                            rate=self.FSAMP,
                            output=True)
        self.quit = Thread(target = self.do)
        self.password = None
        self.username = None

        self.go = True
        
        self.my_name = ""
        self.loginPage()
        
    def main(self):
        self.start()

    def waitForIp(self):
        #wait uneill you get something
        while self.ip==None:
            #make the gui work
            self.login_screen.update_idletasks()
            self.login_screen.update()

            #don't overwork
            sleep(0.1)

    def tryToConnect(self):
        #create the tkinter page to get the ip
        self.msg = Tkinter.Label(self.login_screen, text="Please enter details below", bg="grey")
        self.msg.pack()
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")
        self.login_screen.wm_iconbitmap('pictures\\head.ico')
        self.login_screen.resizable(0, 0)
        ip = Tkinter.StringVar()
        ip_lable = Tkinter.Label(self.login_screen, text="IP * ")
        ip_lable.pack()
        self.ip_entry = Tkinter.Entry(self.login_screen, textvariable=ip)
        self.ip_entry.pack()
        Tkinter.Button(self.login_screen, text="Connect", width=10, height=1, bg="grey", command = lambda: self.getIp(ip.get())).pack()

    def getIp(self,ip): #update the ip
        self.ip = ip       
        self.ip_entry.delete(0, 'end')
        
    def start(self):
        try:
            while True:
                #wait untill you got username and password
                while self.username == None or self.password == None:
                    self.login_screen.update_idletasks()
                    self.login_screen.update()
                    sleep(0.1)
                #send to the server the username and password

                self.clientSocket.send("Connection:" + self.username + "," + self.password)
                #get login status from the server
                l = self.clientSocket.recv(1024) 
                print l
                if l == "Connection accepted": #if connected
                    self.msg.configure(text = "Connection accepted")
                    self.login_screen.destroy()
                    self.my_name = self.username #save my name
                    break
                elif l == "Wrong password":
                    self.msg.configure(text = "Wrong password")
                elif l == "This username does not exist":
                    self.msg.configure(text = "This username does not exist")
                elif l == "This user is taken":
                    self.msg.configure(text ="This user is taken")
                self.username = None
                self.password = None
            self.music() #activate when out of the connection loop
        except:
            os._exit(1)

    def do(self):
        #update the gui so it works
        self.login_screen = Tkinter.Tk()
        self.close()
        while True:
            try:
                self.login_screen.update_idletasks()
                self.login_screen.update()
                sleep(0.1)
            except:
                break
    
    def music(self):
        self.quit.start()
        self.stream.start_stream()
        try:
            l = self.clientSocket.recv(16234) #get the music from the server
            while self.go:
                try:
                    self.stream.write(l) #play the music
                except:
                    #create new stream if there is a problem
                    print "ccccccccccccccccccccccc"
                    self.stream = self.p.open(format=self.FORMAT,
                                channels=2,
                                rate=self.FSAMP,
                                output=True)
                l = self.clientSocket.recv(16234) #get the music from the server
        except:
            pass
        self.clientSocket.close()
        stream.stop_stream()
        stream.close()
        os._exit(1) #close everything

    def close(self):
        #the quit button
        self.login_screen.title("Enjoy")
        self.login_screen.geometry("150x100")
        self.login_screen.wm_iconbitmap('pictures\\head.ico')
        self.login_screen.resizable(0, 0)
        self.login_screen.protocol("WM_DELETE_WINDOW", self.dontClose)
        Tkinter.Button(self.login_screen, text="Quit", width=150, height=100, bg="red3",font="Arial 24 bold", command = self.disconnect).pack()

    def dontClose(self):
        pass
    
    def disconnect(self):
        #disconnect from the server
        self.login_screen.destroy()
        self.clientSocket.send("Disconnect:"+str(self.my_name))
        self.go = False
        
    def loginPage(self):
        #create the login page
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")
        self.login_screen.wm_iconbitmap('pictures\\head.ico')
        self.login_screen.resizable(0, 0)
        username = Tkinter.StringVar()
        password = Tkinter.StringVar()
     
        self.msg = Tkinter.Label(self.login_screen, text="Please enter details below", bg="grey")
        self.msg.pack()
        Tkinter.Label(self.login_screen, text="").pack()
        username_lable = Tkinter.Label(self.login_screen, text="Username * ")
        username_lable.pack()
        self.username_entry = Tkinter.Entry(self.login_screen, textvariable=username)
        self.username_entry.pack()
        password_lable = Tkinter.Label(self.login_screen, text="Password * ")
        password_lable.pack()
        self.password_entry = Tkinter.Entry(self.login_screen, textvariable=password, show='*')
        self.password_entry.pack()
        Tkinter.Label(self.login_screen, text="").pack()
        Tkinter.Button(self.login_screen, text="Login", width=10, height=1, bg="grey", command = lambda: self.login(username.get(),password.get())).pack()
        self.username_entry.focus_set()
        
    def login(self,username,password):
        #update the password and username when trying to login
        self.username = username
        self.password = password
        
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()
        
if __name__ == "__main__":
    x = Client()
    x.main()
