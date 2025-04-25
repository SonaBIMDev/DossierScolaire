# AutoScolarité

AutoScolarité est un outil Python permettant de remplir automatiquement l’intégralité d’un dossier contenant des modèles PDF de scolarité d’un élève en remplaçant des balises (placeholders) par les informations réelles de l’élève.

## Table des matières

1. [Description](#description)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Versions](#versions)  
5. [Contact et support](#contact-et-support)  

## Description

Cet outil parcourt tous les fichiers PDF d’un dossier donné, recherche des balises telles que `[ELEVE_NOM]`, `[ELEVE_DATE_NAISSANCE]`, `[ELEVE_NUM_SECU]`, etc., et les remplace par les valeurs fournies (nom, date de naissance, numéro de sécurité sociale, date de signature, signature du responsable, ...). Chaque fichier modifié est enregistré avec le suffixe `-Modified.pdf` pour préserver l’original.

## Installation

git clone https://github.com/votre-organisation/autoscolarite.git
cd autoscolarite

## Usage

python replace_pdf_text.py \
  --input-folder /chemin/vers/dossier \
  --eleve-nom "Michel Blanc" \
  --eleve-date-naissance "01/01/2005" \
  --eleve-num-secu "1234567890123" \
  --doc-date-signature "25/04/2025" \
  --responsable-signature "Jean Dupont"


## Versions

Major : Indique des changements majeurs ou des modifications incompatibles avec les versions précédentes.
Minor : Représente l'ajout de fonctionnalités compatibles avec les versions antérieures.

#### Dernière version : 1.0

## Contact et support

Société SONABim    
Pierre NAVARRA\
p.navarra@sona-architecture.com\
pierre@sonabim.com\
https://www.linkedin.com/in/pierrenavarra

8, rue de Mayence\
44000 Nantes\
Tel : 06.63.55.73.18\
agence@sona-architecture.com\
http://www.sona-architecture.com/developpement \
http://sonabim.com
