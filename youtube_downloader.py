import yt_dlp as youtube_dl
from pytubefix import Playlist
import subprocess
import os
link_f = []

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")

def main():
    choix = input("Voulez-vous télécharger une playlist ou une vidéo ? (P/V) : ")

    # Condition corrigée pour vérifier l'entrée utilisateur
    while choix not in ["P", "p", "V", "v"]:
        choix = input("Veuillez choisir entre une playlist et une vidéo (P/V) : ")
    
    if choix in ["V", "v"]:
        if not os.path.exists(PATH_VID):
            os.mkdir(PATH_VID)

        Link = input("Entrez le lien de la vidéo : ")
        yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_VID, '%(title)s.%(ext)s')})
        ytv = yt.extract_info(Link, download=True)
        print(f'{ytv["title"]} téléchargée avec succès vers {PATH_VID}')
        subprocess.run("cls", shell=True)
        
    elif choix in ["P", "p"]:
        if not os.path.exists(PATH_PLAY):
            os.mkdir(PATH_PLAY)

        Link = input("Entrez le lien de la playlist : ")
        yt_play = Playlist(Link)

        for i in yt_play.videos:
            link_vid = i.watch_url
            yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s')})
            dl_vid = yt.extract_info(link_vid, download=True)
            print(f'{dl_vid["title"]} téléchargée avec succès vers {PATH_PLAY}')
        subprocess.run("cls", shell=True)

if __name__ == "__main__":
    main()
