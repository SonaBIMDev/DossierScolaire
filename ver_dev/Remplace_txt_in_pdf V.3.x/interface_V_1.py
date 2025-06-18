#!/usr/bin/env python3
from données_ods_V_3_1 import select_doc_file, view_in_doc
from balises_pdf_V_3_1 import select_pdf, extract_variables_in_pdf
from corrélation_pdf_ods_V_3_1 import reusable_balises, search_usable_variables, time_now
from Replace_txt_in_pdf_V_3_1 import replace_text_in_pdf
from rapport_V_3_1 import made_in_heaven
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy

# Définition de la classe principale de l'application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Gestionnaire de Fichiers")
        self.setGeometry(100, 100, 800, 600)

        # Variables d'instance pour stocker les chemins des fichiers
        self.file_ods_path = None
        self.file_pdf_paths = None

        # Création des widgets
        self.add_ods_button = QPushButton("Ajouter un fichier .ods")
        self.add_pdf_button = QPushButton("Ajouter un ou plusieurs fichiers .pdf")
        self.execute_button = QPushButton("Exécuter")

        self.table = QTableWidget()
        self.status_ods_label = QLabel("NON OK")
        self.status_pdf_label = QLabel("NON OK")
        self.status_execute_label = QLabel("PAS PRÊT")

        # Configuration des layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_ods_button)
        button_layout.addWidget(self.add_pdf_button)
        button_layout.addWidget(self.execute_button)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_ods_label)
        status_layout.addWidget(self.status_pdf_label)
        status_layout.addWidget(self.status_execute_label)

        # Configuration du tableau pour qu'il prenne tout l'espace restant
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(status_layout)
        main_layout.addWidget(self.table, stretch=1)  # Utiliser un stretch factor pour le tableau

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

        # Configuration des colonnes du tableau
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nom fichier", "Information du document"])

        # Connexion des signaux et des slots
        self.add_ods_button.clicked.connect(self.add_ods_file)
        self.add_pdf_button.clicked.connect(self.add_pdf_file)
        self.execute_button.clicked.connect(self.execute)

    # Fonction pour vérifier le statut d'exécution
    def check_execute_status(self):
        if self.file_ods_path and self.file_pdf_paths:
            self.status_execute_label.setText("PRÊT")
        else:
            self.status_execute_label.setText("PAS PRÊT")

    # Fonction pour ajouter un fichier ODS
    def add_ods_file(self):
        self.file_ods_path = select_doc_file()
        if self.file_ods_path:
            self.status_ods_label.setText("OK")
            self.check_execute_status()

    # Fonction pour ajouter un ou plusieurs fichiers PDF
    def add_pdf_file(self):
        self.file_pdf_paths = select_pdf()
        if self.file_pdf_paths:
            self.status_pdf_label.setText("OK")
            self.check_execute_status()

    # Fonction pour exécuter le traitement des fichiers
    def execute(self):
        if self.status_execute_label.text() == "PRÊT":
            self.status_execute_label.setText("EN COURS D'EXÉCUTION")
            mapping = view_in_doc(self.file_ods_path)
            balises_par_fichier = extract_variables_in_pdf(self.file_pdf_paths)

            if mapping and balises_par_fichier:
                date = time_now()
                gargamel = reusable_balises(balises_par_fichier)

                if gargamel and date:
                    balises_variables = search_usable_variables(date, gargamel, mapping)

                    if balises_variables:
                        remplacement = replace_text_in_pdf(self.file_pdf_paths, balises_variables)

                        if remplacement:
                            self.status_execute_label.setText("EXÉCUTÉ")
                            messages = made_in_heaven(balises_par_fichier)

                            if messages:
                                self.table.setRowCount(len(messages))

                                for row, (file_name, tags) in enumerate(messages.items()):
                                    tags_text = ", ".join(tags) if tags else "✅ Prêt à l'impression"
                                    self.table.setItem(row, 0, QTableWidgetItem(file_name))
                                    self.table.setItem(row, 1, QTableWidgetItem(tags_text))

# Lancer l'application
app = QApplication([])
app.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec_()
