import socket
import time
import pyaudio
import Tkinter

FORMAT=pyaudio.paInt16
FSAMP = 88800
FRAME_SIZE = 32
p = pyaudio.PyAudio()
clientSocket=socket.socket()
clientSocket.connect(('127.0.0.1',3339))
stream = p.open(format=FORMAT,
                channels=1,
                rate=FSAMP,
                output=True)

stream.start_stream()
while True:
    x = raw_input("what is your username?")
    y = raw_input("what is your password?")
    clientSocket.send("Connection:" + x + "," + y)
    l = clientSocket.recv(32)
    if l=="Connection accepted":
        break
    if l == "Wrong password":
        print "Wrong password"
    if l == "This username does not exist":
        print "This username does not exist"
l = clientSocket.recv(32)
while(l):
    if l == "ServerSentToClient":
        break
    try:
        stream.write(l)
    except:
        stream = p.open(format=FORMAT,
                channels=1,
                rate=FSAMP,
                output=True)
    l = clientSocket.recv(32)

stream.stop_stream()
stream.close()
