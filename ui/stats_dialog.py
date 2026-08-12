from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton
from database import Database

class StatsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NorthType - Istatistikler")
        self.setFixedSize(350, 400)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        total_count, week_count, top_shortcuts = self.db.get_stats()

        layout.addWidget(QLabel(f"Bu Hafta Kullanimi: {week_count} kez"))
        layout.addWidget(QLabel(f"Toplam Engellenen Tekrar: {total_count} kez"))
        layout.addWidget(QLabel("------------------------------------------------"))
        layout.addWidget(QLabel("En Cok Kullanilan Kisayollar:"))

        self.list_widget = QListWidget()
        for sc, count in top_shortcuts:
            self.list_widget.addItem(f"{sc:<15} : {count} kullanim")
        layout.addWidget(self.list_widget)

        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)