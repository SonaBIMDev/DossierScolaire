#!/usr/bin/env python3
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import sys
from balises_pdf import balises
from données_ods import mapping
from balises_pdf import file_pdf_paths

def select_pdf_via_dialog():
    print("Veuillez sélectionner vos fichiers PDF…")
    try:
        root = tk.Tk()
        root.withdraw()
        paths = filedialog.askopenfilenames(
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

def correspond_balises_with_variables(balises, variables):
    if not balises or not variables:
        print("Aucune balise ou variable à traiter.")
        return {}

    correspond = {}
    for balise in balises:
        for variable in variables:
            if balise == variable:
                correspond[balise] = variables[variable]
    return correspond

def replace_text_in_pdf(file_pdf_paths, correspond):
    for file_path in file_pdf_paths:
        doc = fitz.open(str(file_path))
        font = fitz.Font(fontname="helv")  # Helvetica

        for page_num, page in enumerate(doc, start=1):
            for balise, value in correspond.items():
                instances = page.search_for(balise)
                if not instances:
                    continue

                for inst in instances:
                    # 1) Rectangle blanc aux dimensions originales
                    page.draw_rect(inst, fill=(1, 1, 1), color=None)

                    # 2) Taille de police max
                    fontsize = inst.height * 0.8
                    text_width = font.text_length(value, fontsize)
                    box_width = inst.width

                    # 3) Position verticale centrée
                    x = inst.x0
                    y = inst.y0 + (inst.height + fontsize) / 2

                    # 4) On écrit le texte
                    page.insert_text(
                        (x, y),
                        value,
                        fontname="helv",
                        fontsize=fontsize,
                        color=(0, 0, 0),
                        render_mode=0
                    )

        out_path = file_path.with_name(file_path.stem + "-Modified" + file_path.suffix)
        doc.save(str(out_path))
        print(f"Fichier modifié enregistré sous : {out_path}")

    return out_path

def main():
    # Utilisez file_pdf_paths pour obtenir les chemins des fichiers PDF
    pdf_files = file_pdf_paths

    correspond = correspond_balises_with_variables(balises, mapping)
    print(f"Variables correspondantes : {correspond}")
    print(f"Chemin des fichiers : {pdf_files}")

    replace_text_in_pdf(pdf_files, correspond)
    print("Remplacement terminé.")

if __name__ == "__main__":
    main()