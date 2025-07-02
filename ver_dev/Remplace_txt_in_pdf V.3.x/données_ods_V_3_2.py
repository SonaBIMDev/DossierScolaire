#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from odf.text import P
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell

# Fonction pour sélectionner un fichier .ods
def select_doc_file():
    print("Veuillez sélectionner un fichier calculateur")
    # Afficher une boîte de dialogue d'information
    messagebox.showinfo("Information", "Veuillez vérifier que les informations contenues dans le fichier calculateur soient toujours correctes")
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale de tkinter
    # Ouvrir une boîte de dialogue pour sélectionner un fichier calculateur
    file_ods_path = filedialog.askopenfilename(
        title="Veuillez sélectionner un fichier calculateur",
        filetypes=[("Fichier ODS", "*.ods")]
    )
    if file_ods_path:
        print(f"➔ Chemin du fichier calculateur sélectionné : {file_ods_path}")
    return file_ods_path

# Fonction pour lire les informations sur le fichier .ods
def view_in_doc(file_ods_path):
    if not file_ods_path:
        return {}  # Retourner un dictionnaire vide si aucun fichier n'est sélectionné

    try:
        # Charger le document ODS
        doc = load(file_ods_path)
        mapping = {}

        # Parcourir chaque table du document
        for table in doc.getElementsByType(Table):
            # Parcourir chaque ligne de la table
            for row in table.getElementsByType(TableRow):
                cells = row.getElementsByType(TableCell)
                if len(cells) >= 3:
                    value_cells = cells[0]
                    variable_cell = cells[2]
                    # Extraire le texte des paragraphes de la cellule de variable
                    variable_paragraphs = variable_cell.getElementsByType(P)
                    # Extraire le texte des paragraphes de la cellule de valeur
                    value_paragraphs = value_cells.getElementsByType(P)

                    # Vérifier et extraire le texte des paragraphes
                    variable = ''.join(
                        p.firstChild.data if hasattr(p, 'firstChild') and hasattr(p.firstChild, 'data') else ""
                        for p in variable_paragraphs
                    ) if variable_paragraphs else ""
                    value = ''.join(
                        p.firstChild.data if hasattr(p, 'firstChild') and hasattr(p.firstChild, 'data') else ""
                        for p in value_paragraphs
                    ) if value_paragraphs else ""

                    # Assurer que les valeurs sont en string
                    variable = str(variable)
                    value = str(value)
                    mapping[variable] = value
        return mapping
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier calculateur : {e}")
        return {}

# Point d'entrée principal du script
if __name__ == "__main__":
    # Sélectionner un fichier calculateur
    file_ods_path = select_doc_file()
    # Lire et afficher le contenu du fichier calculateur
    mapping = view_in_doc(file_ods_path)

    if not file_ods_path:
        print("❌ Aucun fichier calculateur sélectionné")
    if file_ods_path and mapping:
        print("🔍 Contenu du fichier calculateur :")
        for key, value in mapping.items():
            print(f"  - {key} : {value}")
