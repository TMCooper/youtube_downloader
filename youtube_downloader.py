import yt_dlp as youtube_dl
from pytubefix import Playlist
import subprocess
import os
import json
import sys
import ctypes
import datetime

# Répartir se qui peut l'être dans des class dedier de sorte a avoir un code plus propre et plus lisible (a revoir si c'est vraiment obligatoire)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")
PATH_MP3 = os.path.join(PATH, "Musique")
INDEX = os.path.join(PATH, "index.json")
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

        if not os.path.exists(INDEX):
            with open(INDEX, "w") as f:
                json.dump({}, f)
        index(PATH)

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

            yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_VID, '%(title)s.%(ext)s'),
                                      'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                                      })
            ytv = yt.extract_info(video, download=False)
            title = ytv["title"]

            if mp_v == "mp4":
                if not update_download_index(PATH_VID, ytv):  # Si la vidéo existe déjà
                    print(languages[lang]["alrealy_exist"])
                else:
                    yt.download([video])  # Télécharger
                    print(languages[lang]["success_download"].format(title=title, path=PATH_VID))

            if mp_v == "mp3":
                yt = youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': os.path.join(PATH_MP3, '%(title)s.%(ext)s'),
                                          'postprocessors': [{
                                              'key': 'FFmpegExtractAudio',
                                              'preferredcodec': 'mp3',
                                              'preferredquality': '192',
                                          }]
                                          })
                if not update_download_index(PATH_MP3, ytv):  # Si la vidéo existe déjà
                    print(languages[lang]["alrealy_exist"])
                else:
                    yt.download([video])  # Télécharger
                    print(languages[lang]["success_download"].format(title=title, path=PATH_MP3))

        elif choix in ["p"]:
            if not os.path.exists(PATH_PLAY):
                os.mkdir(PATH_PLAY)

            Link = input(languages[lang]["Requests_user_playlist"])

            yt_play = Playlist(Link)

            for i in yt_play.videos:
                set_proxy(PROXY)
                if mp_v == "mp4":
                    link_vid = i.watch_url

                    yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s'),
                                              'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                                              })

                    dl_vid = yt.extract_info(link_vid, download=False)
                    title = dl_vid["title"]

                    if not update_download_index(PATH_PLAY, dl_vid):  # Si la vidéo existe déjà
                        print(languages[lang]["alrealy_exist"])
                    else:
                        yt.download([link_vid])  # Télécharger
                        print(languages[lang]["success_download"].format(title=title, path=PATH_PLAY))

                if mp_v == "mp3":
                    link_vid = i.watch_url
                    yt = youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': os.path.join(PATH_MP3, '%(title)s.%(ext)s'),
                                              'postprocessors': [{
                                                  'key': 'FFmpegExtractAudio',
                                                  'preferredcodec': 'mp3',
                                                  'preferredquality': '192',
                                              }]
                                              })

                    dl_vid = yt.extract_info(link_vid, download=False)
                    title = dl_vid["title"]

                    if not update_download_index(PATH_MP3, dl_vid):  # Si la vidéo existe déjà
                        print(languages[lang]["alrealy_exist"])
                    else:
                        yt.download([link_vid])  # Télécharger
                        print(languages[lang]["success_download"].format(title=title, path=PATH_MP3))

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
    #subprocess.run(command, shell=True)

def reset_proxy():
    print("reset proxy")
    #subprocess.run('netsh winhttp reset proxy', shell=True)

def is_admin():
    # Vérifie si le script est exécuté avec les droits administratifs
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def index(root_path, output_json="index.json", ignore_patterns=None):
    """
    Crée un index des fichiers dans un dossier et ses sous-dossiers avec des métadonnées.

    Args:
        root_path (str): Chemin du dossier racine à analyser
        output_json (str): Nom du fichier JSON de sortie
        ignore_patterns (list): Liste de patterns de fichiers à ignorer (ex: ['.git', '__pycache__'])

    Returns:
        dict: Dictionnaire contenant l'index des fichiers avec leurs métadonnées
    """
    if not os.path.exists(root_path):
        raise ValueError(f"Le chemin spécifié n'existe pas : {root_path}")

    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', 'index.json']

    index_data = {
        "root_path": root_path,
        "last_updated": datetime.datetime.now().isoformat(),
        "files": [],
        "stats": {
            "total_files": 0,
            "total_size": 0,
            "extensions": {}
        }
    }

    try:
        for root, dirs, files in os.walk(root_path):
            # Ignore les dossiers spécifiés
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            for file_name in files:
                # Ignore les fichiers correspondant aux patterns
                if any(pattern in file_name for pattern in ignore_patterns):
                    continue

                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, root_path)

                try:
                    file_stat = os.stat(full_path)
                    file_ext = os.path.splitext(file_name)[1].lower()

                    # Collecter les métadonnées du fichier
                    file_info = {
                        "name": file_name,
                        "relative_path": rel_path,
                        "size": file_stat.st_size,
                        "modified": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        "extension": file_ext
                    }

                    # Mettre à jour les statistiques
                    index_data["stats"]["total_files"] += 1
                    index_data["stats"]["total_size"] += file_stat.st_size
                    index_data["stats"]["extensions"][file_ext] = index_data["stats"]["extensions"].get(file_ext, 0) + 1

                    index_data["files"].append(file_info)

                except OSError as e:
                    print(f"Erreur lors de l'accès au fichier {full_path}: {e}")
                    continue

        # Trier les fichiers par chemin relatif
        index_data["files"].sort(key=lambda x: x["relative_path"])

        # Sauvegarder l'index dans le fichier JSON
        with open(output_json, "w", encoding="utf-8") as json_file:
            json.dump(index_data, json_file, indent=4, ensure_ascii=False)

        print(f"Index créé avec succès : {len(index_data['files'])} fichiers indexés")
        return index_data

    except Exception as e:
        print(f"Erreur lors de l'indexation : {e}")
        raise

def update_download_index(file_path, video_info):
    """
    Met à jour l'index avec les informations de la vidéo téléchargée et vérifie les doublons
    """
    try:
        # Charger l'index existant
        with open(INDEX, "r", encoding="utf-8") as f:
            index_data = json.load(f)

        # Initialiser la structure si elle n'existe pas
        if "downloads" not in index_data:
            index_data["downloads"] = []

        # Vérifier si la vidéo existe déjà
        video_exists = any(
            download["id"] == video_info["id"] and
            download["path"] == file_path
            for download in index_data["downloads"]
        )

        if video_exists:
            print(f"La vidéo '{video_info['title']}' existe déjà dans {file_path}")
            return False

        # Ajouter les informations de la nouvelle vidéo
        download_info = {
            "title": video_info["title"],
            "id": video_info["id"],
            "path": file_path,
            "download_date": datetime.datetime.now().isoformat(),
            "duration": video_info.get("duration"),
            "format": video_info.get("format")
        }

        # Ajouter à l'index
        index_data["downloads"].append(download_info)

        # Sauvegarder l'index mis à jour
        with open(INDEX, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=4, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'index : {e}")
        return False

if __name__ == "__main__":
    main()
    reset_proxy()  # Réinitialise le proxy après l'exécution principale
    # subprocess.run("cls", shell=True)

    # https://www.youtube.com/watch?v=nZNugmJNFn0