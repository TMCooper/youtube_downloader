import os
import json

# PATH = os.path.dirname(os.path.join(os.path.dirname(__file__))) 
    
class Holo:
    @staticmethod
    def index_dir(PATH_PLAY):
        # travailler sur un system qui enregistrerait les noms de tous les éléments dans une liste json et pourquoi pas effectuer une comparaison a chaque itération et renvoier True ou False en 
        # fonction de si la liste contient le titre de la video afin d'allez plus vite encore qu'avec la biblyothèque
        # Récupère tous les noms de fichiers et dossiers dans le répertoire PATH
        
        # Charger ou initialiser le fichier JSON
        if os.path.exists("index.json"):
            with open("index.json", "r", encoding="utf-8") as index_file:
                try:
                    indexed_files = json.load(index_file)
                except json.JSONDecodeError:
                    indexed_files = {"files": []}
        else:
            indexed_files = {"files": []}

        # Récupérer tous les fichiers dans le répertoire
        files_and_dirs = os.listdir(PATH_PLAY)
        new_files = []

        for file in files_and_dirs:
            if file.endswith(".mp4") or file.endswith(".mp3"):
                if file not in indexed_files["files"]:
                    indexed_files["files"].append(file)
                    new_files.append(file)

        # Mettre à jour le fichier JSON
        with open("index.json", "w", encoding="utf-8") as index_file:
            json.dump(indexed_files, index_file, ensure_ascii=False, indent=4)

        # Retourner True si de nouveaux fichiers ont été ajoutés, sinon False
        return len(new_files) > 0