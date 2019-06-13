from __future__ import unicode_literals
import youtube_dl
import os

#to make everything work download http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

class musicDownloader():
    def __init__(self):
        pass

    def downloadSong(self,url,title):
        temp = os.listdir(os.getcwd()+"\\songs")
        for name in temp:
            if str(name).split(".")[0]==title:
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
                info_dict = ydl.extract_info(url)
                #name = 'songs\\' + title + '.wav'
                #os.rename('songs\\aaaa.wav', name)
            return "download completed"
        except:
            return "something is wrong with the url"
