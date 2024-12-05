import yt_dlp as youtube_dl
from pytubefix import Playlist
import subprocess
import os
import json
import sys
import ctypes

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")
PATH_MP3 = os.path.join(PATH, "Musique")
PROXY = 'http://218.155.31.188:8080'

def main():
    try:
        if is_admin():
            # Si le script est lancé en tant qu'administrateur, continue l'exécution
            set_proxy(PROXY)
        else:
            # Si le script n'est pas lancé en tant qu'administrateur, redémarre-le avec élévation
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            return  # Sort de la fonction pour éviter d'exécuter le reste du code

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
        
        
        if choix in ["v"]:
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)
            


            Link = input(languages[lang]["Requests_user_link"])

            ID_V = Link.split("watch?v=")[1].split("&")[0]
            video = (f'https://www.youtube.com/watch?v={ID_V}')

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

            subprocess.run("cls", shell=True)
            
        elif choix in ["p"]:
            if not os.path.exists(PATH_PLAY):
                os.mkdir(PATH_PLAY)

            Link = input(languages[lang]["Requests_user_playlist"])

            yt_play = Playlist(Link)

            for i in yt_play.videos:
                set_proxy('https://218.155.31.188:8080')
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

            subprocess.run("cls", shell=True)
        
        elif choix in ["q"]:
            print(languages[lang]["Exit_q"])
            exit()
    
    except KeyboardInterrupt:
        print(languages[lang]["keyboard_interupt"])
    
    except KeyError:
        print(languages[lang]["error_key"])
    
    finally:
        reset_proxy()  # Réinitialise le proxy à la fin

def set_proxy(proxy_url):
    command = f'netsh winhttp set proxy proxy-server="{proxy_url}"'
    subprocess.run(command, shell=True)

def reset_proxy():
    subprocess.run('netsh winhttp reset proxy', shell=True)

def is_admin():
    # Vérifie si le script est exécuté avec les droits administratifs
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    main()
    reset_proxy()  # Réinitialise le proxy après l'exécution principale
    subprocess.run("cls", shell=True)