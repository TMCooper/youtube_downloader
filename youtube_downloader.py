from pytubefix import YouTube, Playlist
import os
play_list = []

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")

def main():
    choix = input("Voullez vous télécharger une playlist ou une vidéo ? P/V : ")

    while(choix != "P" or choix == "p" or choix == "V" or choix == "v"):
        choix = input("Veulliez choisir entre une playlist et une vidéo (P/V) : ")
        if(choix == "P" or choix == "p"):
            break
        if(choix == "V" or choix == "v"):
            break
    
    if(choix == "V" or choix == "v"):
        if not os.path.exists(PATH_VID):
            os.mkdir(PATH_VID)

        Link = input("Entrer le lien de la vidéo : ")
        yt = YouTube(Link)
        yt.streams.filter(progressive=True,
                          file_extension="mp4").first().download(
                              output_path=PATH_VID,filename=(f'{yt.title}.mp4'))
        print(f'{yt.title} Télécharger avec succès vers {PATH_VID}')

    if(choix == "P" or choix == "p"):
        if not os.path.exists(PATH_PLAY):
            os.mkdir(PATH_PLAY)
        
        Link = input("Entrer le lien de la playlist : ")
        ytp = Playlist(Link)
        print('Number of videos in playlist: %s' % len(ytp.video_urls))

        for video_url in ytp.video_urls:
            print(video_url)
            play_list.append(video_url)
        
        for i in play_list:
            try:
                yt = YouTube(i)
                print('Téléchargement lien : ' + i)
                print('Téléchargement video : '+ yt.streams[0].title)
            except:
                print("Erreur Connection")

            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
            stream.download(PATH_PLAY)
        print("Tache fini")

if __name__ == "__main__":
    main()
