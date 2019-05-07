import socket
import time
import pyaudio

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
clientSocket.send("Connection:dror,1234")
l = clientSocket.recv(32)
frames=[]
while(l):
    if l == "ServerSentToClient":
        break
    frames.append(l)
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
