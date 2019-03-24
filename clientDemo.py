import socket
import time
import pyaudio

FORMAT=pyaudio.paInt16
FSAMP = 88800
FRAME_SIZE = 16
p = pyaudio.PyAudio()
clientSocket=socket.socket()
clientSocket.connect(('192.168.1.106',3334))
stream = p.open(format=FORMAT,
                channels=1,
                rate=FSAMP,
                output=True)

stream.start_stream() 
l = clientSocket.recv(16)
frames=[]
while(l):
    if l == "ServerSentToClient":
        break
    frames.append(l)
    stream.write(l)
    l = clientSocket.recv(16)

stream.stop_stream()
stream.close()
