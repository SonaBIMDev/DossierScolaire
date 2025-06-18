#!/usr/bin/env python3
from datetime import datetime
from balises_pdf_V_3_1 import extract_variables_in_pdf, select_pdf
from données_ods_V_3_1 import view_in_doc, select_doc_file

# Fonction pour collecter toutes les balises du dictionnaire donné
def reusable_balises(balises_par_fichier):
    gargamel = []
    # Parcourir chaque ensemble de balises et les ajouter à la liste
    for balises in balises_par_fichier.values():
        gargamel.append(balises)
    return gargamel

# Fonction pour obtenir la date actuelle au format "dd-mm-yyyy"
def time_now():
    date = datetime.now().strftime("%d-%m-%Y")
    return date

# Fonction pour rechercher les variables utilisables et les mapper à leurs valeurs correspondantes
def search_usable_variables(date, gargamel, mapping):
    balises_variables = {}
    # Parcourir chaque ensemble de balises
    for les_chaussons_a_gargamel in gargamel:
        # Parcourir chaque balise dans l'ensemble
        for var in les_chaussons_a_gargamel:
            var_without_spaces = var.replace(" ", "")
            print(f"  - {var_without_spaces} = {var}")
            # Parcourir chaque clé dans le mapping
            for keys in mapping.keys():
                # Remplacer la balise de date par la date actuelle
                if var_without_spaces == "[800]":
                    balises_variables[var] = date
                else:
                    # Si la clé correspond à la balise, mapper la valeur
                    if keys == var_without_spaces:
                        balises_variables[var] = mapping[keys]
    return balises_variables

# Fonction pour imprimer le dictionnaire des variables et leurs valeurs correspondantes
def print_balises_variables(balises_variables):
    print("🔍 dictionnaire des valeurs à changer :")
    for key, value in balises_variables.items():
        print(f"  - {key} : {value}")

# Point d'entrée principal du script
if __name__ == "__main__":
    # Sélectionner les fichiers PDF et extraire les variables de ceux-ci
    file_pdf_paths = select_pdf()
    balises_par_fichier = extract_variables_in_pdf(file_pdf_paths)

    # Sélectionner le fichier ODS et afficher son contenu
    file_ods_path = select_doc_file()
    mapping = view_in_doc(file_ods_path)

    # Vérifier si les balises et le mapping sont disponibles
    if balises_par_fichier and mapping:
        date = time_now()
        print(f"date : {date}")

        # Collecter toutes les balises
        gargamel = reusable_balises(balises_par_fichier)
        if gargamel:
            print(f"🧼 balises nettoyées :")

            # Rechercher les variables utilisables et les mapper
            balises_variables = search_usable_variables(date, gargamel, mapping)
            if balises_variables:
                # Imprimer le dictionnaire des variables et leurs valeurs correspondantes
                print_balises_variables(balises_variables)
