import yt_dlp as youtube_dl
from pytubefix import Playlist
import subprocess
import os
import json


PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")

def main():
    try:
        valid_languages = ["en", "fr"]

        with open('languages.json', 'r') as lang_file:
            languages = json.load(lang_file)

        print(f"Available languages: {', '.join(valid_languages).upper()}")
        lang = input("What is your language ? : ").lower()

        while lang not in valid_languages:
            print(f"Available languages: {', '.join(valid_languages).upper()}")
            lang = input("Please select your language: ").lower()
        
        print(languages[lang]["Exit_q"])
        choix = input(languages[lang]["User_request_P_V"]).lower()

        # Condition corrigée pour vérifier l'entrée utilisateur
        while choix not in ["p", "v", "q"]:
            choix = input(languages[lang]["Force_user_request_P_V"]).lower()
        
        if choix in ["v"]:
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)

            Link = input(languages[lang]["Requests_user_link"])

            ID_V = Link.split("watch?v=")[1].split("&")[0]
            video = (f'https://www.youtube.com/watch?v={ID_V}')

            yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_VID, '%(title)s.%(ext)s'),
                                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                        })
            ytv = yt.extract_info(video, download=True)
            title = ytv["title"] 
            print(languages[lang]["success_download"].format(title=title, path=PATH_VID))
            subprocess.run("cls", shell=True)
            
        elif choix in ["p"]:
            if not os.path.exists(PATH_PLAY):
                os.mkdir(PATH_PLAY)

            Link = input(languages[lang]["Requests_user_playlist"])

            yt_play = Playlist(Link)

            for i in yt_play.videos:
                link_vid = i.watch_url
                yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s'),
                                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                        })
                dl_vid = yt.extract_info(link_vid, download=True)
                title = dl_vid["title"]
                print(languages[lang]["success_download"].format(title=title, path=PATH_PLAY))
            subprocess.run("cls", shell=True)
        
        elif choix in ["q"]:
            print(languages[lang]["Exit_q"])
            exit()

    except KeyboardInterrupt:       
        print(languages[lang]["keyboard_interupt"])

if __name__ == "__main__":
    main()
