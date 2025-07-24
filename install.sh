#!/bin/bash

# Set title (not supported in all shells)
# echo -ne "\033]0;Lanceur d'application Python\007"

# Check if virtual environment exists
if [ ! -d "./Youtube_Downloader" ]; then
  echo "[ERREUR] Environnement virtuel 'Youtube_Downloader' introuvable."
  python3 -m venv Youtube_Downloader
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
  echo "[ERREUR] Le fichier 'requirements.txt' est introuvable."
  exit 1
fi

# Check if main.py exists
if [ ! -f "youtube_downloader.py" ]; then
  echo "[ERREUR] Le script principal 'youtube_downloader.py' est introuvable."
  exit 1
fi

# Activate virtual environment
source ./Youtube_Downloader/bin/activate

echo "[1/3] Activation de l'environnement virtuel..."

echo
echo "[2/3] Installation des dépendances depuis requirements.txt..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
  echo "[ERREUR] L'installation des dépendances a échoué."
  deactivate
  exit 1
fi

echo
echo --------------------------------------------------
echo

echo "Le script est terminé. Appuyez sur Entrée pour quitter."
read
deactivate
