import socket
import time
import pyaudio
import Tkinter
from threading import Thread
from time import sleep
import os

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
        self.quit = Thread(target = self.do)
        self.password = None
        self.username = None
        self.loginPage()
        
    def main(self):
        self.start()
        
    def start(self):
        try:
            while True:
                while self.username == None or self.password == None:
                    self.login_screen.update_idletasks()
                    self.login_screen.update()
                    sleep(0.1)
                self.clientSocket.send("Connection:" + self.username + "," + self.password)
                l = self.clientSocket.recv(32)
                if l=="Connection accepted":
                    self.msg.configure(text = "Connection accepted")
                    self.login_screen.destroy()
                    break
                if l == "Wrong password":
                    self.msg.configure(text = "Wrong password")
                if l == "This username does not exist":
                    self.msg.configure(text = "This username does not exist")
                self.username = None
                self.password = None
            self.music()
        except:
            os._exit(1)

    def do(self):
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
        os._exit(1)

    def close(self):
        self.login_screen.title("Enjoy")
        self.login_screen.geometry("150x100")
        self.login_screen.wm_iconbitmap('pictures\\head.ico')
        self.login_screen.resizable(0, 0)
        self.login_screen.protocol("WM_DELETE_WINDOW", self.disconnect)
        Tkinter.Button(self.login_screen, text="Quit", width=150, height=100, bg="red3",font="Arial 24 bold", command = self.disconnect).pack()
    def disconnect(self):
        self.login_screen.destroy()
        self.clientSocket.send("Disconnect:")
        
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
