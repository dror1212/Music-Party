import pyaudio
import wave
import Tkinter
import time
import os


class Recorder():
    def __init__(self,root):
        self.root = root
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.record = False
        self.audio = pyaudio.PyAudio()
        self.screen = None
        self.allowedChars = [' ', '','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','-','.','_',',','\\','/','*','1','2','3','4','5','6','7','8','9','0']

    def start(self,name):
        try:
            # start Recording
            WAVE_OUTPUT_FILENAME = "songs\\" + name + ".wav"

            for char in name:
                if char not in self.allowedChars:
                    return "You can name the songs only in english"
                
            temp = os.listdir(os.getcwd()+"\\songs")
            
            for name2 in temp:
                if str(name2).split(".")[0]==name:
                    return "This song is already exist"
                
            self.record = True
            stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                    rate=self.RATE, input=True,
                                    frames_per_buffer=32)
            print "recording..."
            frames = []
            while self.record:
                self.screen.update_idletasks()
                self.screen.update()
                data = stream.read(4)
                frames.append(data)
            
                  
            # stop Recording
            stream.stop_stream()
            stream.close()
             
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(self.CHANNELS)
            waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            waveFile.setframerate(self.RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            print "finished recording"
            return "finished recording"
        except:
            return "something is wrong"
        
    def down(self):
        self.screen.destroy()
        self.screen = None

    def Record(self):
        name = self.name_entry.get()
        if len(name)>0:
            if not self.record:
                self.btn.config(text = "Stop")
                self.msg.config(text = "Recording")
                check = self.start(name)
                if check!="finished recording":
                    self.btn.config(text = "Record")
                self.msg.config(text = check)
                self.name_entry.delete(0, 'end')
            else:
                self.record = False
                #self.msg.config(text = "Click the button to record")
                self.btn.config(text = "Record")
                self.name_entry.delete(0, 'end')
        else:
            if not self.record:
                self.msg.config(text = "You must enter a name to record")
            else:
                self.record = False
                #self.msg.config(text = "Click the button to record")
                self.btn.config(text = "Record")
                self.name_entry.delete(0, 'end')
                
    def Page(self):
        if self.screen == None:
            self.screen = Tkinter.Toplevel(self.root)
            self.screen.title("Record")
            self.screen.geometry("300x250")
            self.screen.wm_iconbitmap('pictures\\head.ico')
            self.screen.protocol("WM_DELETE_WINDOW", self.down)
            self.screen.resizable(0, 0)
            name = Tkinter.StringVar()
     
            self.msg = Tkinter.Label(self.screen, text="Click the button to record", bg="grey")
            self.msg.pack()
            Tkinter.Label(self.screen, text="").pack()
            name_lable = Tkinter.Label(self.screen, text="Name * ")
            name_lable.pack()
            self.name_entry = Tkinter.Entry(self.screen, textvariable=name)
            self.name_entry.pack()
            Tkinter.Label(self.screen, text="").pack()
            self.btn = Tkinter.Button(self.screen, text="Record", width=10, height=1, bg="grey", command = self.Record)
            self.btn.pack()
            self.name_entry.focus_set()
