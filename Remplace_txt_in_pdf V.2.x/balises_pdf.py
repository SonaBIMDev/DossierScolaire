import re
import sys
import tkinter as tk
import fitz  # PyMuPDF
from pathlib import Path
from tkinter.filedialog import askopenfilenames

def select_pdf():
    print("Veuillez sélectionner votre fichier PDF…")
    try:
        root = tk.Tk()
        root.withdraw()
        paths = askopenfilenames(
            title="Sélectionnez un ou plusieurs fichiers PDF",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        root.destroy()
        if not paths:
            print("Aucun fichier sélectionné. Fin du programme.")
            sys.exit(1)
        return [Path(path) for path in paths]
    except ImportError:
        print("Tkinter non disponible.", file=sys.stderr)
        sys.exit(1)

def extract_variables_in_pdf(file_pdf_paths):
    balises = set()

    for file_path in file_pdf_paths:
        try:
            # Ouvrir un fichier PDF à la fois
            doc = fitz.open(file_path)  
            for page in doc:
                text = page.get_text()
                found_variables = re.findall(r'\[([^\]]+)\]', text)
                # inclut les crochets dans la variable trouver
                balises.update(f'[{var}]' for var in found_variables)
            doc.close()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier {file_path}: {e}")
    
    return balises

file_pdf_paths = select_pdf()
balises = extract_variables_in_pdf(file_pdf_paths)
print(f"balises trouvées : {balises}")