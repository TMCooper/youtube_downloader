import yt_dlp as youtube_dl
from pytubefix import Playlist
import subprocess
import os


PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")

def main():
    try:
        lang = input("What is your language ? (FR/EN) : ").lower()

        while lang not in ["fr", "en"]:
            lang = input("What is your language ? FR or EN").lower()
        
        if lang in ["en"]:
            print("To exit the program type Q")
            choix = input("Do you want to download a playlist or video? (P/V) : ").lower()

        else:
            print("Pour quiter le programme tapper Q")
            choix = input("Voulez-vous télécharger une playlist ou une vidéo ? (P/V) : ").lower()

        # Condition corrigée pour vérifier l'entrée utilisateur
        while choix not in ["p", "v", "q"]:
            if lang not in ["fr", "en"]:
                choix = input("Please choose between a playlist and a video (P/V) : ").lower()

            else:
                choix = input("Veuillez choisir entre une playlist et une vidéo (P/V) : ").lower()
        
        if choix in ["v"]:
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)

            if lang in ["en"]:
                Link = input("Enter the video link : ")
            
            else:
                print("Entrez le lien de la vidéo : ")

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
            
            if lang in ["en"]:
                Link = input("Enter the playlist link:")
            else:
                Link = input("Entrez le lien de la playlist : ")

            yt_play = Playlist(Link)

            for i in yt_play.videos:
                link_vid = i.watch_url
                yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s'),
                                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                        })
                dl_vid = yt.extract_info(link_vid, download=True)
                if lang in["en"]:
                    print(f'{dl_vid["title"]} successfully download to {PATH_PLAY}')

                else:
                    print(f'{dl_vid["title"]} téléchargée avec succès vers {PATH_PLAY}')

            subprocess.run("cls", shell=True)
        
        elif choix in ["q"]:
            if lang in ["en"]:
                print("Exit...")
            else:
                print("Sortie...")
            exit

    except KeyboardInterrupt:
        if lang in ["en"]:
            print("\nThe user typed CTRL + Stop the program...")
        else:
            print("\nL'utilisateur a saisit CTRL + C arret du programme ...")

if __name__ == "__main__":
    main()
