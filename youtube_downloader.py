import yt_dlp as youtube_dl
from pytubefix import Playlist
import subprocess
import os


PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")

def main():
    try:
        print("Pour quiter le programme tapper Q")
        choix = input("Voulez-vous télécharger une playlist ou une vidéo ? (P/V) : ").lower()

        # Condition corrigée pour vérifier l'entrée utilisateur
        while choix not in ["p", "v", "q"]:
            choix = input("Veuillez choisir entre une playlist et une vidéo (P/V) : ").lower()
        
        if choix in ["v"]:
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)

            Link = input("Entrez le lien de la vidéo : ")
            ID_V = Link.split("watch?v=")[1].split("&")[0]
            video = (f'https://www.youtube.com/watch?v={ID_V}')

            yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_VID, '%(title)s.%(ext)s'),
                                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                        })
            ytv = yt.extract_info(video, download=True)
            print(f'{ytv["title"]} téléchargée avec succès vers {PATH_VID}')
            subprocess.run("cls", shell=True)
            
        elif choix in ["p"]:
            if not os.path.exists(PATH_PLAY):
                os.mkdir(PATH_PLAY)

            Link = input("Entrez le lien de la playlist : ")
            yt_play = Playlist(Link)

            for i in yt_play.videos:
                link_vid = i.watch_url
                yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s'),
                                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                        })
                dl_vid = yt.extract_info(link_vid, download=True)
                print(f'{dl_vid["title"]} téléchargée avec succès vers {PATH_PLAY}')

            subprocess.run("cls", shell=True)
        
        elif choix in ["q"]:
            exit

    except KeyboardInterrupt:
        print("\nL'utilisateur a saisit CTRL + C arret du programme ...")

if __name__ == "__main__":
    main()
