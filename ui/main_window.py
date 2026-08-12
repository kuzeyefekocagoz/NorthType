import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                               QMessageBox, QCheckBox, QComboBox)
from PySide6.QtCore import Qt, QMetaObject, Q_ARG, Slot
from database import Database
from ui.shortcut_dialog import ShortcutDialog
from ui.tray import TrayManager
from ui.stats_dialog import StatsDialog
from ui.suggestion_popup import SuggestionPopup
from utils import set_autostart

class MainWindow(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.engine.suggestion_callback = self.update_suggestions_ui
        
        self.db = Database()
        
        self.setWindowTitle("NorthType - Akilli Metin Kisayollari")
        self.setFixedSize(450, 580)
        
        self.suggestion_popup = SuggestionPopup(self)
        self.suggestion_popup.shortcut_selected.connect(self.on_suggestion_selected)

        self.init_ui()
        self.load_shortcuts()

        self.tray = TrayManager(self)
        set_autostart(True)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Kisayol ara...")
        self.search_input.textChanged.connect(self.filter_shortcuts)
        top_layout.addWidget(self.search_input)

        self.category_filter = QComboBox()
        self.category_filter.addItem("Tum Kategoriler")
        self.category_filter.addItems(ShortcutDialog.CATEGORIES)
        self.category_filter.currentIndexChanged.connect(self.filter_shortcuts)
        top_layout.addWidget(self.category_filter)
        
        main_layout.addLayout(top_layout)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.edit_shortcut)
        main_layout.addWidget(self.list_widget)

        mid_layout = QHBoxLayout()
        self.autostart_check = QCheckBox("Windows Baslangicinda Calistir")
        self.autostart_check.setChecked(True)
        self.autostart_check.stateChanged.connect(self.update_autostart)
        mid_layout.addWidget(self.autostart_check)

        self.stats_btn = QPushButton("Istatistikler")
        self.stats_btn.clicked.connect(self.show_stats)
        mid_layout.addWidget(self.stats_btn)
        
        main_layout.addLayout(mid_layout)

        bottom_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Sil")
        self.delete_btn.clicked.connect(self.delete_shortcut)
        
        self.add_btn = QPushButton("+ Kisayol Ekle")
        self.add_btn.clicked.connect(self.add_shortcut)

        bottom_layout.addWidget(self.delete_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.add_btn)
        
        main_layout.addLayout(bottom_layout)

    def load_shortcuts(self):
        self.list_widget.clear()
        shortcuts = self.db.get_all_shortcuts()
        for row in shortcuts:
            item_id, shortcut, replacement, category, is_sensitive, enabled, usage_count = row
            
            display_rep = "[Hassas Veri]" if is_sensitive else replacement.splitlines()[0]
            display_text = f"[{category}] {shortcut:<12} ->  {display_rep}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, row)
            self.list_widget.addItem(item)

    def filter_shortcuts(self):
        text = self.search_input.text().lower()
        selected_cat = self.category_filter.currentText()

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            row_data = item.data(Qt.UserRole)
            sc, rep, cat, is_sens = row_data[1], row_data[2], row_data[3], row_data[4]

            matches_text = text in sc.lower() or text in rep.lower()
            matches_cat = (selected_cat == "Tum Kategoriler" or cat == selected_cat)

            if matches_text and matches_cat:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def add_shortcut(self):
        dialog = ShortcutDialog(self)
        if dialog.exec():
            sc, rep, cat, sens = dialog.get_data()
            success = self.db.add_shortcut(sc, rep, cat, sens)
            if success:
                self.load_shortcuts()
            else:
                QMessageBox.warning(self, "Hata", "Bu kisayol zaten mevcut!")

    def edit_shortcut(self, item):
        row_data = item.data(Qt.UserRole)
        item_id, shortcut, replacement, category, is_sensitive, enabled, _ = row_data
        
        dialog = ShortcutDialog(self, shortcut, replacement, category, is_sensitive)
        if dialog.exec():
            sc, rep, cat, sens = dialog.get_data()
            self.db.update_shortcut(item_id, sc, rep, cat, sens)
            self.load_shortcuts()

    def delete_shortcut(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Uyari", "Lutfen silinecek bir kisayol secin!")
            return
            
        row_data = selected_item.data(Qt.UserRole)
        item_id = row_data[0]
        
        confirm = QMessageBox.question(self, "Onay", "Secili kisayolu silmek istediginize emin misiniz?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_shortcut(item_id)
            self.load_shortcuts()

    def show_stats(self):
        dialog = StatsDialog(self)
        dialog.exec()

    def update_suggestions_ui(self, suggestions):
        QMetaObject.invokeMethod(self, "_safe_show_suggestions", 
                                  Qt.QueuedConnection, 
                                  Q_ARG(object, suggestions))

    @Slot(object)
    def _safe_show_suggestions(self, suggestions):
        self.suggestion_popup.update_suggestions(suggestions)

    def on_suggestion_selected(self, shortcut):
        pass

    def update_autostart(self):
        set_autostart(self.autostart_check.isChecked())

    def closeEvent(self, event):
        event.ignore()
        self.hide()