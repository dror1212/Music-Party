import pyaudio
import wave
import Tkinter
import time

class Recorder():
    def __init__(self,root):
        self.root = root
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.WAVE_OUTPUT_FILENAME = "file.wav"
        self.record = False
        self.audio = pyaudio.PyAudio()
        self.screen = None

    def start(self):
        # start Recording
        self.record = True
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        print "recording..."
        frames = []
        while self.record:
            self.screen.update_idletasks()
            self.screen.update()
            data = stream.read(self.CHUNK)
            frames.append(data)
        
              
        # stop Recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
         
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print "finished recording"
        
    def down(self):
        self.screen.destroy()
        self.screen = None

    def Record(self):
        if not self.record:
            self.btn.config(text = "Stop")
            self.msg.config(text = "Recording")
            self.start()
        else:
            self.record = False
            self.msg.config(text = "Click the button to record")
            self.btn.config(text = "Record")
                
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
            self.btn = Tkinter.Button(self.screen, text="Record", width=10, height=1, bg="grey", command = lambda: self.Record())
            self.btn.pack()
            self.name_entry.focus_set()
