from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                               QTextEdit, QComboBox, QCheckBox, QHBoxLayout, 
                               QPushButton, QMessageBox)

class ShortcutDialog(QDialog):
    CATEGORIES = ["Kisisel", "Kod", "E-posta", "Okul", "Is", "Adresler", "Sik kullanilanlar"]

    def __init__(self, parent=None, shortcut="", replacement="", category="Kisisel", is_sensitive=0):
        super().__init__(parent)
        self.setWindowTitle("Kisayol Yonetimi")
        self.setFixedSize(380, 420)
        
        self.init_ui(shortcut, replacement, category, is_sensitive)

    def init_ui(self, shortcut, replacement, category, is_sensitive):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Kisayol (Orn: :mail, :bug, :pyclass)"))
        self.shortcut_input = QLineEdit(shortcut)
        layout.addWidget(self.shortcut_input)

        layout.addWidget(QLabel("Kategori"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.CATEGORIES)
        if category in self.CATEGORIES:
            self.category_combo.setCurrentText(category)
        layout.addWidget(self.category_combo)

        layout.addWidget(QLabel("Karsilik gelen metin / Sablon / Kod"))
        self.replacement_input = QTextEdit()
        self.replacement_input.setPlainText(replacement)
        layout.addWidget(self.replacement_input)

        self.sensitive_check = QCheckBox("Hassas veri (Sifre/Token - Gizle)")
        self.sensitive_check.setChecked(bool(is_sensitive))
        layout.addWidget(self.sensitive_check)

        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Iptal")
        self.save_btn = QPushButton("Kaydet")
        
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.validate_and_save)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def validate_and_save(self):
        sc = self.shortcut_input.text().strip()
        rep = self.replacement_input.toPlainText().strip()

        if not sc.startswith(":"):
            QMessageBox.warning(self.parent(), "Uyari", "Kisayol ':' karakteri ile basmalidir!")
            return
        if not sc or not rep:
            QMessageBox.warning(self.parent(), "Uyari", "Alanlar bos birakilamaz!")
            return

        self.accept()

    def get_data(self):
        sc = self.shortcut_input.text().strip()
        rep = self.replacement_input.toPlainText().strip()
        cat = self.category_combo.currentText()
        sens = 1 if self.sensitive_check.isChecked() else 0
        return sc, rep, cat, sens