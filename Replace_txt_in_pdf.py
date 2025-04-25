#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

import fitz  # PyMuPDF

def select_pdf_via_dialog():
    print("Veuillez sélectionner votre fichier PDF…")
    try:
        import tkinter as tk
        from tkinter.filedialog import askopenfilename

        root = tk.Tk()
        root.withdraw()
        path = askopenfilename(
            title="Sélectionnez un fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        root.destroy()
        if not path:
            print("Aucun fichier sélectionné. Fin du programme.")
            sys.exit(1)
        return Path(path)
    except ImportError:
        print("Tkinter non disponible.", file=sys.stderr)
        sys.exit(1)

def prompt_if_missing(prompt_text: str) -> str:
    while True:
        val = input(prompt_text).strip()
        if val:
            return val
        print("⚠️ Valeur requise.")

def replace_text_in_pdf(input_path: Path, search_text: str, replace_text: str) -> Path:
    """
    Masque chaque placeholder par un rectangle blanc de la largeur d'origine,
    puis y dessine le texte de remplacement en réduisant la taille de police
    pour qu'il rentre exactement dans cette largeur.
    """
    doc = fitz.open(str(input_path))
    font = fitz.Font(fontname="helv")  # Helvetica
    replaced = False

    for page_num, page in enumerate(doc, start=1):
        instances = page.search_for(search_text)
        if not instances:
            continue

        print(f"🔍 « {search_text} » trouvé {len(instances)} fois sur la page {page_num}")
        replaced = True

        for inst in instances:
            # 1) Rectangle blanc aux dimensions originales
            page.draw_rect(inst, fill=(1, 1, 1), color=None)

            # 2) Taille de police max
            fontsize = inst.height * 0.8
            # Mesure de la largeur du texte à cette taille
            text_width = font.text_length(replace_text, fontsize)
            box_width = inst.width  # inst.x1 - inst.x0

            # 3) Si ça déborde, on réduit la taille
            if text_width > box_width:
                fontsize = fontsize * box_width / text_width

            # 4) Position verticale centrée
            x = inst.x0
            y = inst.y0 + (inst.height + fontsize) / 2

            # 5) On écrit le texte
            page.insert_text(
                (x, y),
                replace_text,
                fontname="helv",
                fontsize=fontsize,
                color=(0, 0, 0),
                render_mode=0
            )

        print(f" • Remplacement effectué sur la page {page_num}")

    if not replaced:
        print("⚠️ Aucun texte trouvé à remplacer.")
    out_path = input_path.with_name(input_path.stem + "-Modified" + input_path.suffix)
    doc.save(str(out_path))
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Remplace un texte dans un PDF en utilisant PyMuPDF."
    )
    parser.add_argument("pdf_path", type=Path, nargs="?",
                        help="(optionnel) Chemin vers le PDF")
    parser.add_argument("search_text", nargs="?",
                        help="(optionnel) Texte à trouver (ex. [ELEVE_NOM])")
    parser.add_argument("replace_text", nargs="?",
                        help="(optionnel) Texte de remplacement")
    args = parser.parse_args()

    # Sélection du PDF
    if args.pdf_path:
        pdf_file = args.pdf_path
        if not pdf_file.is_file():
            print(f"❌ Le fichier {pdf_file} n'existe pas.")
            sys.exit(1)
    else:
        pdf_file = select_pdf_via_dialog()

    # Saisie interactive du search et replace si manquants
    search = args.search_text or prompt_if_missing("Entrez le texte à rechercher : ")
    replace = args.replace_text or prompt_if_missing("Entrez le texte de remplacement : ")

    out_pdf = replace_text_in_pdf(pdf_file, search, replace)
    print(f"\n✅ Fichier modifié enregistré sous :\n   {out_pdf}")

if __name__ == "__main__":
    main()
