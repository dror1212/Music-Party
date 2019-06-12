from __future__ import unicode_literals
import youtube_dl

#to make everything work download http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

class musicDownloader():
    def __init__(self):
        pass

    def downloadSong(self,url):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return "download completed"
        except:
            return "something is wrong with the url"
