from __future__ import unicode_literals
import youtube_dl
import os
import Tkinter
from threading import Thread

#to make everything work download http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

class musicDownloader():
    def __init__(self,root):
        self.allowedChars = [' ', '','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','-','.','_',',','\\','/','*','1','2','3','4','5','6','7','8','9','0']
        self.root = root
        self.downloading_screen = None

    def downloadSong(self,url,title):
        print title
        if "www.youtube.com/watch?v=" not in url:
            return "something is wrong with the url"
        temp = os.listdir(os.getcwd()+"\\songs")

        for char in title:
            if char not in self.allowedChars:
                return "You can name the songs only in english"
        

        for name2 in temp:
            if str(name2).split(".")[0]==title:
                return "This song is already exist"
        print temp
        
        name = 'songs\\' + title
        
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '720',
                }],
                'outtmpl': name +'.%(ext)s'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return "download completed"
        except:
            return "something is wrong"
        
    def dow(self):
        self.downloading_screen.destroy()
        self.downloading_screen = None

    def Page(self):
        if self.downloading_screen == None:
            self.downloading_screen = Tkinter.Toplevel(self.root)
            self.downloading_screen.title("Download")
            self.downloading_screen.geometry("300x250")
            self.downloading_screen.wm_iconbitmap('pictures\\head.ico')
            self.downloading_screen.protocol("WM_DELETE_WINDOW", self.dow)
            self.downloading_screen.resizable(0, 0)
            link = Tkinter.StringVar()
            name = Tkinter.StringVar()
     
            self.holder = Tkinter.Label(self.downloading_screen, text="Please enter details below", bg="grey")
            self.holder.pack()
            Tkinter.Label(self.downloading_screen, text="").pack()
            link_lable = Tkinter.Label(self.downloading_screen, text="URL * ")
            link_lable.pack()
            self.link_entry = Tkinter.Entry(self.downloading_screen, textvariable=link)
            self.link_entry.pack()
            name_lable = Tkinter.Label(self.downloading_screen, text="Name For The Song * ")
            name_lable.pack()
            self.name_entry = Tkinter.Entry(self.downloading_screen, textvariable=name)
            self.name_entry.pack()
            Tkinter.Label(self.downloading_screen, text="").pack()
            Tkinter.Button(self.downloading_screen, text="Download", width=10, height=1, bg="grey",command = lambda: self.download(link.get(),name.get())).pack()
            self.link_entry.focus_set()

    def download(self,link,name):
        if name!="" and link!="":
            self.link_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.link_entry.focus_set()
            down = Thread(target = self.d,args = (link,name,))
            down.start()
        
    def d(self,link,name):
        check = self.downloadSong(link,name)
        self.holder.config(text=check)
