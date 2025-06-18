#!/usr/bin/env python3
import re
import sys
import tkinter as tk
import fitz  # PyMuPDF
from pathlib import Path
from tkinter.filedialog import askopenfilenames

# Fonction pour sélectionner un ou plusieurs fichiers PDF
def select_pdf():
    print("Veuillez sélectionner un ou plusieurs fichier PDF")
    try:
        root = tk.Tk()
        root.withdraw()
        paths = askopenfilenames(
            title="Veuillez sélectionnez un ou plusieurs fichiers PDF",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        root.destroy()
        if not paths:
            print("❌​ Aucun(s) fichier(s) PDF sélectionné(s)")
            sys.exit(1)
        return [Path(path) for path in paths]
    except ImportError:
        print("❌ Tkinter non disponible", file=sys.stderr)
        sys.exit(1)

# Fonction pour extraire les variables dans les fichiers PDF
def extract_variables_in_pdf(file_pdf_paths):
    balises = set()
    for file_path in file_pdf_paths:
        try:
            # Ouvrir un fichier PDF à la fois
            doc = fitz.open(file_path)
            for page in doc:
                text = page.get_text()
                found_variables = re.findall(r'\[([^\]]+)\]', text)
                # Inclut les crochets dans la variable trouvée
                balises.update(f'[{var}]' for var in found_variables)
            doc.close()
        except Exception as e:
            print(f"❌​ Erreur lors de l'ouverture du ou des fichiers PDF {file_path}: {e}")

    return balises

# Sélectionne les fichiers PDF
file_pdf_paths = select_pdf()
print(f"➔  Chemin du ou des fichiers PDF : {file_pdf_paths}")
# Extrait les balises des fichiers PDF
balises = extract_variables_in_pdf(file_pdf_paths)
print(f"🔍​ balises trouvées : {balises}")