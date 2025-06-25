#!/usr/bin/env python3
import re 
import sys 
import tkinter as tk 
import fitz  # PyMuPDF
from pathlib import Path  
from tkinter.filedialog import askopenfilenames  

# Fonction pour sélectionner un ou plusieurs fichiers PDF
def select_pdf():
    print("Veuillez sélectionner un ou plusieurs fichiers PDF")
    try:
        # Initialiser une fenêtre tkinter
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre principale

        # Ouvrir une boîte de dialogue pour sélectionner un ou plusieurs fichiers PDF
        paths = askopenfilenames(
            title="Veuillez sélectionner un ou plusieurs fichiers PDF",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        paths = tuple(paths)  # Convertir les chemins sélectionnés en un tuple
        root.destroy()  # Fermer la fenêtre tkinter

        # Vérifier si des fichiers ont été sélectionnés
        if not paths:
            print("❌ Aucun(s) fichier(s) PDF sélectionné(s)")

        # Retourner les chemins des fichiers sélectionnés sous forme de Path
        return [Path(path) for path in paths]
    except ImportError:
        # Gérer l'erreur si tkinter n'est pas disponible
        print("❌ Tkinter non disponible", file=sys.stderr)
        sys.exit(1)  # Quitter le programme avec un code d'erreur

# Fonction pour extraire les variables dans les fichiers PDF
def extract_variables_in_pdf(file_pdf_paths):
    balises_par_fichier = {}  # Dictionnaire pour stocker les balises par fichier
    for file_path in file_pdf_paths:
        balises = set()  # Ensemble pour stocker les balises uniques du fichier
        try:
            # Ouvrir un fichier PDF à la fois
            doc = fitz.open(file_path)
            for page in doc:
                # Extraire le texte de la page
                text = page.get_text()
                # Trouver toutes les variables dans le texte (entre crochets)
                found_variables = re.findall(r'\[([^\]]+)\]', text)
                # Inclure les crochets dans la variable trouvée
                balises.update(f'[{var}]' for var in found_variables)
            doc.close()  # Fermer le document PDF
            balises_par_fichier[file_path] = balises  # Stocker les balises pour ce fichier
        except Exception as e:
            # Gérer les erreurs lors de l'ouverture ou du traitement du fichier PDF
            print(f"❌ Erreur lors de l'ouverture du ou des fichiers PDF {file_path}: {e}")

    return balises_par_fichier  # Retourner le dictionnaire des balises par fichier

# Fonction pour afficher les balises trouvées par fichier
def print_balises(balises_par_fichier):
    print("🔍 balises trouvées par fichier :")
    for key, values in balises_par_fichier.items():
        print(f"  {key}")  # Afficher le chemin du fichier
        for value in values:
            print(f"  - {value}")  # Afficher chaque balise trouvée dans le fichier

# Point d'entrée principal du script
if __name__ == "__main__":
    # Sélectionner les fichiers PDF
    file_pdf_paths = select_pdf()
    if file_pdf_paths:
        # Extraire les variables des fichiers PDF sélectionnés
        balises_par_fichier = extract_variables_in_pdf(file_pdf_paths)
        if balises_par_fichier:
            # Afficher les balises trouvées par fichier
            print_balises(balises_par_fichier)
