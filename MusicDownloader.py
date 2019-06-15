from __future__ import unicode_literals
import youtube_dl
import os

#to make everything work download http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

class musicDownloader():
    def __init__(self):
        self.allowedChars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','-','.','_',',','\\','/','*']
        pass

    def downloadSong(self,url,title):
        if "www.youtube.com/watch?v=" not in url:
            return "something is wrong with the url"
        temp = os.listdir(os.getcwd()+"\\songs")

        for char in title:
            if char not in self.allowedChars:
                return "You can name the songs only in english"
        name = 'songs\\' + title

        for name in temp:
            if str(name).split(".")[0]==title:
                return "This song is already exist"
        print temp
        
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
                info_dict = ydl.extract_info(url)
                #name = 'songs\\' + title + '.wav'
                #os.rename('songs\\aaaa.wav', name)
            return "download completed"
        except:
            return "something is wrong"
