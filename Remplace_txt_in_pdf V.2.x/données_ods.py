#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
from odf.text import P
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell

# Fonction pour sélectionner un fichier .ods
def select_doc_file():
    root = tk.Tk()
    root.withdraw()
    file_ods_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier .ods",
        filetypes=[("Fichier ODS", "*.ods")]
    )
    if file_ods_path:
        print(f"Fichier sélectionné : {file_ods_path}")
    else:
        print("Aucun fichier sélectionné")
    return file_ods_path

# Fonction pour lire les informations dans le fichier .ods
def view_in_doc(file_ods_path):
    if not file_ods_path:
        return {}

    try:
        doc = load(file_ods_path)
        mapping = {}

        for table in doc.getElementsByType(Table):
            for row in table.getElementsByType(TableRow):
                cells = row.getElementsByType(TableCell)
                if len(cells) >= 2:
                    variable_cell = cells[0]
                    value_cells = cells[1]
                    # ne regarde que les deux première colones 

                    # Extraction du texte des paragraphes
                    variable_paragraphs = variable_cell.getElementsByType(P)
                    value_paragraphs = value_cells.getElementsByType(P)

                    # Vérification des paragraphes
                    variable = ''.join(
                        p.firstChild.data if hasattr(p, 'firstChild') and hasattr(p.firstChild, 'data') else ""
                        for p in variable_paragraphs
                    ) if variable_paragraphs else ""
                    value = ''.join(
                        p.firstChild.data if hasattr(p, 'firstChild') and hasattr(p.firstChild, 'data') else ""
                        for p in value_paragraphs
                    ) if value_paragraphs else ""

                    # Assure que les valeurs sont en string
                    variable = str(variable)
                    value = str(value)
                    mapping[variable] = value
        return mapping
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return {}

# Sélectionne le fichier .ods
file_ods_path = select_doc_file()

# Lit les informations dans le fichier .ods
mapping = view_in_doc(file_ods_path)

# Affiche les résultats
print("Contenu du fichier .ods :", mapping)