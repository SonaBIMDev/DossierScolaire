#!/usr/bin/env python3
from balises_pdf_V_3_2 import extract_variables_in_pdf, select_pdf
import os
import pandas as pd

# Fonction pour traiter les balises des fichiers PDF et générer des messages d'erreur
def made_in_heaven(balises_par_fichier):
    # Dictionnaire pour stocker les messages post-traitement pour chaque fichier
    messages_post_traitement_pdf = {}

    # Parcourir chaque fichier et ses balises associées
    for key, gargamel in balises_par_fichier.items():
        # Utiliser un ensemble pour stocker les messages uniques pour chaque fichier
        message = set()

        # Extraire le nom du fichier à partir du chemin
        file_name = os.path.basename(key)

        # Afficher le nom du fichier en cours de traitement
        print(f"➔ {file_name}")

        # Parcourir chaque balise du fichier
        for les_chaussons_a_gargamel in gargamel:
            # Supprimer les espaces de la balise pour la comparaison
            var_without_spaces = les_chaussons_a_gargamel.replace(" ", "")

            # Vérifier chaque balise et ajouter un message approprié si nécessaire
            if var_without_spaces == "[900]":
                print("⚠️ Attention, la signature de l'élève est manquante")
                message.add("⚠️ Signature de l'élève")
            elif var_without_spaces == "[901]":
                print("⚠️ Attention, la signature du responsable légal est manquante")
                message.add("⚠️ Signature du responsable légal")
            elif var_without_spaces == "[902]":
                print("⚠️ Attention, la signature du père est manquante")
                message.add("⚠️ Signature du père")
            elif var_without_spaces == "[903]":
                print("⚠️ Attention, la signature de la mère est manquante")
                message.add("⚠️ Signature de la mère")
            elif var_without_spaces == "[904]":
                print("⚠️ Attention, la signature du tuteur est manquante")
                message.add("⚠️ Signature du tuteur")
            elif var_without_spaces == "[910]":
                print("⚠️ Attention, le montant de l'argent est manquant")
                message.add("⚠️ Montant argent")
            elif var_without_spaces == "[911]":
                print("⚠️ Attention, l'autorisation est manquante")
                message.add("⚠️ Autorisation")
            elif var_without_spaces == "[999]":
                print("⚠️ Attention, un élément autre est manquant")
                message.add("⚠️ Autre")

        # Ajouter les messages au dictionnaire avec le nom du fichier comme clé
        messages_post_traitement_pdf[file_name] = list(message)

    # Retourner le dictionnaire des messages post-traitement
    return messages_post_traitement_pdf

# Fonction pour afficher les messages dans un DataFrame pandas
def afficher_messages(messages):
    # Liste pour stocker les données à afficher
    data = []
    # Parcourir chaque fichier et ses statuts
    for fichier, statuts in messages.items():
        # Si aucun statut n'est présent, le fichier est prêt à l'impression
        if not statuts:
            data.append({"Document": fichier, "Statut": "✅ Prêt à l'impression"})
        else:
            # Sinon, joindre les statuts avec des sauts de ligne
            data.append({"Document": fichier, "Statut": "\n".join(statuts)})

    # Créer un DataFrame à partir des données et l'afficher
    df = pd.DataFrame(data)
    print(df.to_markdown(index=False))

# Point d'entrée principal du script
if __name__ == "__main__":
    # Sélectionner les fichiers PDF
    file_pdf_paths = select_pdf()
    # Extraire les balises des fichiers PDF sélectionnés
    balises_par_fichier = extract_variables_in_pdf(file_pdf_paths)
    # Traiter les balises et obtenir les messages post-traitement
    messages = made_in_heaven(balises_par_fichier)
    # Afficher les messages post-traitement
    print(messages)
    # Afficher les messages dans un tableau
    afficher_messages(messages)