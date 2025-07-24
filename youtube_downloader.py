import platform
from pytubefix import Playlist
from function.Cardinal import *
from function.Yui import *
from function.Holo import *
import os

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")
PATH_MP3 = os.path.join(PATH, "Musique")
PROXY = 'http://218.155.31.188:8080'

def main():
    try:
        if Yui.is_admin():
            # Si le script est lancé en tant qu'administrateur, continue l'exécution
            Yui.set_proxy(PROXY)
        else:
            # Si le script n'est pas lancé en tant qu'administrateur, redémarre-le avec élévation
            Yui.run_as_admin()
            return  # Sort de la fonction pour éviter d'exécuter le reste du code
            

        lang, languages, choix, mp_v = Cardinal.basic()
        
        
        if choix in ["v"]:
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)

            Link = input(languages[lang]["Requests_user_link"])

            ID_V = Link.split("watch?v=")[1].split("&")[0]
            video = (f'https://www.youtube.com/watch?v={ID_V}')

            Cardinal.Video_downloader(video, mp_v, lang, languages, PATH_VID, PATH_MP3)

            subprocess.run("cls", shell=True)
            
        elif choix in ["p"]:
            if not os.path.exists(PATH_PLAY):
                os.mkdir(PATH_PLAY)

            Link = input(languages[lang]["Requests_user_playlist"])

            yt_play = Playlist(Link)

            Cardinal.Playlist_downloader(yt_play.videos, mp_v, lang, languages, PATH_PLAY, PATH_MP3)

            subprocess.run("cls", shell=True)
        
        elif choix in ["q"]:
            print(languages[lang]["Exit_q"])
            exit()
    
    except KeyboardInterrupt:
        print(languages[lang]["keyboard_interupt"])
    
    except KeyError:
        print(languages[lang]["error_key"])
    
    finally:
        Yui.reset_proxy()  # Réinitialise le proxy à la fin

if __name__ == "__main__":
    main()
    Yui.reset_proxy()  # Réinitialise le proxy après l'exécution principale
    subprocess.run("cls", shell=True)