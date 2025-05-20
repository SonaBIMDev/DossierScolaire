#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import fitz  # PyMuPDF

def select_pdf_via_dialog():
    print("Veuillez sélectionner votre fichier PDF…")
    try:
        import tkinter as tk
        from tkinter.filedialog import askopenfilenames

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

def prompt_if_missing(prompt_text: str) -> str:
    while True:
        val = input(prompt_text).strip()
        if val:
            return val
        print("⚠️ Valeur requise. Réessayez.")

def replace_text_in_pdf(doc, search_text: str, replace_text: str):
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

def main():
    parser = argparse.ArgumentParser(
        description="Remplace un texte dans un PDF en utilisant PyMuPDF."
    )
    parser.add_argument("pdf_path", type=Path, nargs="?",
                        help="(optionnel) Chemin vers le PDF")
    args = parser.parse_args()

    # Sélection des PDFs
    if args.pdf_path:
        pdf_files = [args.pdf_path]
        if not pdf_files[0].is_file():
            print(f"❌ Le fichier {pdf_files[0]} n'existe pas.")
            sys.exit(1)
    else:
        pdf_files = select_pdf_via_dialog()

    # Charger les documents PDF
    docs = [fitz.open(str(pdf_file)) for pdf_file in pdf_files]

    while True:
        search = prompt_if_missing("Entrez le texte à rechercher (ou 'stop' pour arrêter) : ")
        if search.lower() == 'stop':
            break
        replace = prompt_if_missing("Entrez le texte de remplacement : ")

        for doc in docs:
            replace_text_in_pdf(doc, search, replace)

    # Enregistrer les documents modifiés
    for doc, pdf_file in zip(docs, pdf_files):
        out_pdf = pdf_file.with_name(f"{pdf_file.stem}-Modified{pdf_file.suffix}")
        doc.save(str(out_pdf))
        print(f"\n✅ Fichier modifié enregistré sous :\n   {out_pdf}")

if __name__ == "__main__":
    main()
