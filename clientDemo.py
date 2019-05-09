import socket
import time
import pyaudio
import Tkinter
from threading import Thread
from time import sleep

class Client():
    def __init__(self):
        self.login_screen = Tkinter.Tk()
        self.FORMAT=pyaudio.paInt16
        self.FSAMP = 88800
        self.FRAME_SIZE = 32
        self.p = pyaudio.PyAudio()
        self.clientSocket=socket.socket()
        self.clientSocket.connect(('127.0.0.1',3539))
        self.stream = self.p.open(format=self.FORMAT,
                            channels=1,
                            rate=self.FSAMP,
                            output=True)
        self.music_control = Thread(target = self.start)
        self.password = None
        self.username = None
        self.loginPage()
        
    def main(self):
        self.music_control.start()
        self.login_screen.mainloop()
        
    def start(self):
        try:
            while True:
                while self.username == None or self.password == None:
                    sleep(0.1)
                self.clientSocket.send("Connection:" + self.username + "," + self.password)
                l = self.clientSocket.recv(32)
                if l=="Connection accepted":
                    self.msg.configure(text = "Connection accepted")
                    break
                if l == "Wrong password":
                    self.msg.configure(text = "Wrong password")
                if l == "This username does not exist":
                    self.msg.configure(text = "This username does not exist")
                self.username = None
                self.password = None
            self.music()
        except:
            pass

    def music(self):
        self.stream.start_stream()
        try:
            l = self.clientSocket.recv(32)
            while(l):
                if l == "ServerSentToClient":
                    break
                try:
                    self.stream.write(l)
                except:
                    self.stream = self.p.open(format=self.FORMAT,
                                channels=1,
                                rate=self.FSAMP,
                                output=True)
                l = self.clientSocket.recv(32)
        except:
            pass
        stream.stop_stream()
        stream.close()

    def loginPage(self):
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
        self.username = username
        self.password = password
        
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()
        
if __name__ == "__main__":
    x = Client()
    x.main()
