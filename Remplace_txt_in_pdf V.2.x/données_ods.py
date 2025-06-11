#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from odf.text import P
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell

# Fonction pour sélectionner un fichier .ods
def select_doc_file():
    print("Veuillez sélectionner un fichier ODS")
    root = tk.Tk()
    root.withdraw()
    file_ods_path = filedialog.askopenfilename(
        title="Veuillez sélectionnez un fichier ODS",
        filetypes=[("Fichier ODS", "*.ods")]
    )
    if file_ods_path:
        print(f"➔  Chemin du fichier ODS sélectionné : {file_ods_path}")
    return file_ods_path

# Fonction pour lire les informations sur le fichier .ods
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
                    # Ne regarde que les deux premières colonnes

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
        print(f"❌​ Erreur lors de la lecture du fichier ODS : {e}")
        return {}

file_ods_path = select_doc_file()
mapping = view_in_doc(file_ods_path)

if not file_ods_path:
    print("❌​ ​Aucun fichier ODS sélectionné")
if file_ods_path and mapping:
    print("🔍​ Contenu du fichier ODS :", mapping)