#!/usr/bin/env python3
import fitz  # PyMuPDF
from corrélation_pdf_ods_V_3_2 import search_usable_variables, time_now, reusable_balises
from balises_pdf_V_3_2 import select_pdf, extract_variables_in_pdf
from données_ods_V_3_2 import view_in_doc, select_doc_file 

# Fonction pour remplacer le texte dans les fichiers PDF
def replace_text_in_pdf(file_pdf_paths, balises_variables):
    # Parcourir chaque fichier PDF
    for file_path in file_pdf_paths:
        # Ouvrir le fichier PDF
        doc = fitz.open(str(file_path))
        # Définir la police à utiliser
        font = fitz.Font(fontname="helv")  # Helvetica

        # Parcourir chaque page du document
        for page_num, page in enumerate(doc, start=1):
            # Parcourir chaque balise et sa valeur associée
            for balise, value in balises_variables.items():
                # Rechercher les instances de la balise sur la page
                instances = page.search_for(balise)
                if not instances:
                    continue  # Si la balise n'est pas trouvée, passer à la suivante

                # Pour chaque instance de la balise trouvée
                for inst in instances:
                    # 1) Dessiner un rectangle blanc aux dimensions originales pour masquer l'ancien texte
                    page.draw_rect(inst, fill=(1, 1, 1), color=None)

                    # 2) Calculer la taille de police maximale possible
                    fontsize = inst.height * 0.8
                    text_width = font.text_length(value, fontsize)
                    box_width = inst.width

                    # 3) Si le texte dépasse, réduire la taille de la police
                    if text_width > box_width:
                        fontsize = fontsize * box_width / text_width

                    # 4) Calculer la position verticale centrée
                    x = inst.x0
                    y = inst.y0 + (inst.height + fontsize) / 2

                    # 5) Insérer le nouveau texte
                    page.insert_text(
                        (x, y),
                        value,
                        fontname="helv",
                        fontsize=fontsize,
                        color=(0, 0, 0),
                        render_mode=0
                    )

        # Sauvegarder le fichier modifié avec un nouveau nom
        out_path = file_path.with_name(file_path.stem + "-Modified" + file_path.suffix)
        doc.save(str(out_path))
        print(f"💾 Fichier modifié enregistré sous : {out_path}")
    return out_path

# Point d'entrée principal du script
if __name__ == "__main__":
    # Sélectionner les fichiers PDF et les balises à remplacer
    pdf_files = select_pdf()
    balises_par_fichier = extract_variables_in_pdf(pdf_files)

    file_ods_path = select_doc_file()
    mapping = view_in_doc(file_ods_path)

    if pdf_files and mapping:
        date = time_now()
        gargamel = reusable_balises(balises_par_fichier)
        if gargamel:
            balises_variables = search_usable_variables(date, gargamel, mapping)
            # Remplacer le texte dans les fichiers PDF
            replace_text_in_pdf(pdf_files, balises_variables)
            print("✅ Remplacement terminé")
