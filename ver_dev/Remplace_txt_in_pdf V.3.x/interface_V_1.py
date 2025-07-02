#!/usr/bin/env python3
from données_ods_V_3_2 import select_doc_file, view_in_doc
from balises_pdf_V_3_2 import select_pdf, extract_variables_in_pdf
from corrélation_pdf_ods_V_3_2 import reusable_balises, search_usable_variables, time_now
from Replace_txt_in_pdf_V_3_2 import replace_text_in_pdf
from rapport_V_3_2 import made_in_heaven
import tkinter as tk
from tkinter import messagebox
from PyQt5.QtGui import QCursor,QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy, QProgressBar

# Classe de travailleur pour exécuter des tâches longues dans un thread séparé
class Worker(QThread):
    finished = pyqtSignal()
    result_ready = pyqtSignal(dict)
    progress_updated = pyqtSignal(int)  # Signal pour mettre à jour la barre de progression
    status_execute = pyqtSignal(str)

    def __init__(self, file_ods_path, file_pdf_paths):
        super().__init__()
        self.file_ods_path = file_ods_path
        self.file_pdf_paths = file_pdf_paths

    def run(self):
        # Exécuter la tâche longue ici
        self.progress_updated.emit(15)  # Mettre à jour la progression à 15%
        self.status_execute.emit("Tache en cours : Extraction des balises...")
        balises_par_fichier = extract_variables_in_pdf(self.file_pdf_paths)

        self.progress_updated.emit(40)  # Mettre à jour la progression à 40%
        self.status_execute.emit("Tache en cours : Extraction des information contenues dans le fichier calculateur...")       
        mapping = view_in_doc(self.file_ods_path)

        if mapping and balises_par_fichier:
            self.progress_updated.emit(50)  # Mettre à jour la progression à 60%
            self.status_execute.emit("Tache en cours : Récupération de la date...")
            date = time_now()

            self.progress_updated.emit(70)  # Mettre à jour la progression à 70%
            self.status_execute.emit("Tache en cours : Corélation des balises entre le fichier PDF et calculateur...")
            gargamel = reusable_balises(balises_par_fichier)

            if gargamel and date:
                self.progress_updated.emit(80)  # Mettre à jour la progression à 80%
                self.status_execute.emit("Tache en cours : Corélation entre les balises et les informations du fichier calculateur...")
                balises_variables = search_usable_variables(date, gargamel, mapping)

                if balises_variables:
                    self.progress_updated.emit(90)  # Mettre à jour la progression à 90%
                    self.status_execute.emit("Tache en cours : Remplacement des balises par les informations du fichier calculateur...")
                    remplacement = replace_text_in_pdf(self.file_pdf_paths, balises_variables)

                    if remplacement:
                        self.progress_updated.emit(100)  # Mettre à jour la progression à 100%
                        self.status_execute.emit("")        
                        messages = made_in_heaven(balises_par_fichier)
                        self.result_ready.emit(messages)

        self.finished.emit()

# Définition de la classe principale de l'application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Dossier scolaire")
        self.setGeometry(100, 100, 800, 600)

        # Variables d'instance pour stocker les chemins des fichiers
        self.file_ods_path = None
        self.file_pdf_paths = None

        # Création des widgets
        self.add_pdf_button = QPushButton("Ajouter un ou plusieurs fichiers .pdf")
        self.add_ods_button = QPushButton("Ajouter le fichier calculateur")
        self.execute_button = QPushButton("Exécuter")
        self.reset = QPushButton("Réinitialiser l'application")

        self.status_ods_label = QLabel("NON OK")
        self.status_pdf_label = QLabel("NON OK")
        self.status_execute_label = QLabel("PAS PRÊT")
        self.status_reset_label = QLabel("")
        self.status_execute_label_info = QLabel("")

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)  # Centrer le texte dans la barre de progression
        self.setWindowIcon(QIcon("C:/Users/SONA/AppData/Roaming/source/DossierScolaire/ver_dev/Remplace_txt_in_pdf V.3.x/1234.ico"))

        self.table = QTableWidget()
        self.status_ods_label = QLabel("NON OK")
        self.status_pdf_label = QLabel("NON OK")
        self.status_execute_label = QLabel("PAS PRÊT")
        self.status_reset_label = QLabel("")

        # Configuration des layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_pdf_button)
        button_layout.addWidget(self.add_ods_button)
        button_layout.addWidget(self.execute_button)
        button_layout.addWidget(self.reset)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_pdf_label)
        status_layout.addWidget(self.status_ods_label)
        status_layout.addWidget(self.status_execute_label)
        status_layout.addWidget(self.status_reset_label)

        # Configuration du tableau pour qu'il prenne tout l'espace restant
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(status_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_execute_label_info)
        main_layout.addWidget(self.table)  # Utiliser un stretch factor pour le tableau
        self.progress_bar.setValue(0)

        # Définir le facteur d'étirement pour le tableau
        main_layout.setStretchFactor(self.table, 1)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

        # Configuration des colonnes du tableau
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nom fichier", "Rapport du document"])

        # Définir la largeur des colonnes et la hauteur des lignes
        self.table.setColumnWidth(0, 280)  # Largeur de la première colonne
        self.table.setColumnWidth(1, 500)  # Largeur de la deuxième colonne
        self.table.verticalHeader().setDefaultSectionSize(40)  # Hauteur des lignes

        # Connexion des signaux et des slots
        self.add_pdf_button.clicked.connect(self.add_pdf_file)
        self.add_ods_button.clicked.connect(self.add_ods_file)
        self.execute_button.clicked.connect(self.execute)
        self.reset.clicked.connect(self.reset_application)

    # Fonction pour vérifier le statut d'exécution
    def check_execute_status(self):
        if self.file_ods_path and self.file_pdf_paths:
            self.status_execute_label.setText("PRÊT")
        else:
            self.status_execute_label.setText("PAS PRÊT")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def status_execute(self, status):
        self.status_execute_label_info.setText(status)

    # Fonction pour ajouter un fichier ODS
    def add_ods_file(self):
        self.status_ods_label.setText("NON OK")
        self.file_ods_path = select_doc_file()
        if self.file_ods_path:
            self.status_ods_label.setText("OK")
        else:
            self.status_ods_label.setText("NON OK")
        self.check_execute_status()

    # Fonction pour ajouter un ou plusieurs fichiers PDF
    def add_pdf_file(self):
        self.status_pdf_label.setText("NON OK")
        self.file_pdf_paths = select_pdf()
        if self.file_pdf_paths:
            self.status_pdf_label.setText("OK")
        else:
            self.status_pdf_label.setText("NON OK")
        self.check_execute_status()

    def reset_application(self):
        if not self.status_execute_label.text() == "EN COURS D'EXÉCUTION":
            response = messagebox.askquestion("Question", "Êtes-vous sûr de vouloir continuer?")
            if response == 'yes':
                # Réinitialiser les variables d'instance
                self.file_ods_path = None
                self.file_pdf_paths = None

                # Réinitialiser les labels de statut
                self.status_ods_label.setText("NON OK")
                self.status_pdf_label.setText("NON OK")
                self.status_execute_label.setText("PAS PRÊT")

                # Réinitialiser la barre de progression
                self.progress_bar.setValue(0)

                # Réinitialiser le tableau
                self.table.setRowCount(0)
        else:
            messagebox.showwarning("Erreur", "Impossible de réinitialiser l'application pendant l'exécution")

    # Fonction pour exécuter le traitement des fichiers
    def execute(self):
        if self.status_execute_label.text() == "PRÊT":
            self.status_execute_label.setText("EN COURS D'EXÉCUTION")
            self.progress_bar.setValue(0)
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # Changer le curseur en mode chargement
            self.worker = Worker(self.file_ods_path, self.file_pdf_paths)
            self.worker.progress_updated.connect(self.update_progress)
            self.worker.status_execute.connect(self.status_execute)
            self.worker.result_ready.connect(self.on_worker_result)
            self.worker.finished.connect(self.on_worker_finished)
            self.worker.start()
        elif not self.file_ods_path and not self.file_pdf_paths:
            messagebox.showwarning("Erreur", "Veuillez ajouter un fichier calculateur et un ou plusieurs fichiers PDF avant d'exécuter")
        elif not self.file_ods_path:
            messagebox.showwarning("Erreur", "Il vous manque le fichier calculateur")
        elif not self.file_pdf_paths:
            messagebox.showwarning("Erreur", "Il vous manque le ou les fichiers PDF")
        elif self.status_execute_label.text() == "EXÉCUTÉ":
            response = messagebox.askquestion("Question", "Êtes-vous sûr de vouloir continuer?")
            if response == 'yes':
                self.status_execute_label.setText("EN COURS D'EXÉCUTION")
                self.progress_bar.setValue(0)
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # Changer le curseur en mode chargement
                self.worker = Worker(self.file_ods_path, self.file_pdf_paths)
                self.worker.progress_updated.connect(self.update_progress)
                self.worker.status_execute.connect(self.status_execute)
                self.worker.result_ready.connect(self.on_worker_result)
                self.worker.finished.connect(self.on_worker_finished)
                self.worker.start()

    def on_worker_result(self, messages):
        if messages:
            self.table.setRowCount(len(messages))
            for row, (file_name, tags) in enumerate(messages.items()):
                tags_text = ", ".join(tags) if tags else "✅ Prêt à l'impression"
                self.table.setItem(row, 0, QTableWidgetItem(file_name))
                self.table.setItem(row, 1, QTableWidgetItem(tags_text))
                QApplication.restoreOverrideCursor()  # Rétablir le curseur normal

    def on_worker_finished(self):
        self.status_execute_label.setText("EXÉCUTÉ")

# Lancer l'application
app = QApplication([])
app.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec_()