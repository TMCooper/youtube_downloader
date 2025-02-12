from function.Yui import *
import yt_dlp as youtube_dl
import os
import json

class Cardinal:
    def Playlist_downloader(yt_play_videos, mp_v, lang, languages, PATH_PLAY, PATH_MP3):
        for i in yt_play_videos:
                Yui.set_proxy('https://218.155.31.188:8080')
                
                if mp_v == "mp4" : 
                    link_vid = i.watch_url
                    yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s'),
                                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                            })
                    dl_vid = yt.extract_info(link_vid, download=True)
                    title = dl_vid["title"]
                    
                    print(languages[lang]["success_download"].format(title=title, path=PATH_PLAY))
                    
                    subprocess.run("cls", shell=True)

                if mp_v == "mp3":
                    link_vid = i.watch_url
                    yt = youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': os.path.join(PATH_MP3, '%(title)s.%(ext)s'),
                                            'postprocessors': [{
                                                'key': 'FFmpegExtractAudio',
                                                'preferredcodec': 'mp3',
                                                'preferredquality': '192',
                                                }]
                                                })
                    dl_vid = yt.extract_info(link_vid, download=True)
                    title = dl_vid["title"]
                    
                    print(languages[lang]["success_download"].format(title=title, path=PATH_PLAY))
                    
                    subprocess.run("cls", shell=True)
        
    def Video_downloader(video, mp_v, lang, languages, PATH_VID, PATH_MP3):
        if mp_v == "mp4":
            yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_VID, '%(title)s.%(ext)s'),
                                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                            })
            ytv = yt.extract_info(video, download=True)
            title = ytv["title"] 
            print(languages[lang]["success_download"].format(title=title, path=PATH_VID))
            
        if mp_v == "mp3":
            yt = youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': os.path.join(PATH_MP3, '%(title)s.%(ext)s'),
                                          'postprocessors': [{
                                            'key': 'FFmpegExtractAudio',
                                            'preferredcodec': 'mp3',
                                            'preferredquality': '192',
                                            }]
                                            })
            ytv = yt.extract_info(video, download=True)
            title = ytv["title"] 
            print(languages[lang]["success_download"].format(title=title, path=PATH_VID))

    
    def basic():
        valid_languages = ["en", "fr"]

        with open('languages.json', 'r') as lang_file:
            languages = json.load(lang_file)

        print(f"Available languages: {', '.join(valid_languages).upper()}")
        lang = input("What is your language ? : ").lower()

        while lang not in valid_languages:
            print(f"Available languages: {', '.join(valid_languages).upper()}")
            lang = input("Please select your language: ").lower()

        choix = input(languages[lang]["User_request_P_V"]).lower()

        # Condition corrigée pour vérifier l'entrée utilisateur
        while choix not in ["p", "v", "q"]:
            choix = input(languages[lang]["Force_user_request_P_V"]).lower()

        mp_v = input(languages[lang]["check_extention"]).lower()
        
        while mp_v not in ["mp3", "mp4"]:
            mp_v = input(languages[lang]["error_mp_v"])
        
        return lang, languages, choix, mp_v