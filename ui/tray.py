from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QStyle
from PySide6.QtGui import QAction
from PySide6.QtCore import QObject
import sys

class TrayManager(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.tray_icon = QSystemTrayIcon()
        
        icon = self.main_window.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray_icon.setIcon(icon)
        
        menu = QMenu()
        
        self.toggle_action = QAction("Durdur", self)
        self.toggle_action.triggered.connect(self.toggle_engine)
        
        stats_action = QAction("İstatistikler", self)
        stats_action.triggered.connect(self.main_window.show_stats)

        open_action = QAction("Aç", self)
        open_action.triggered.connect(self.main_window.show)
        
        quit_action = QAction("Çıkış", self)
        quit_action.triggered.connect(self.quit_app)
        
        menu.addAction(open_action)
        menu.addAction(stats_action)
        menu.addAction(self.toggle_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def quit_app(self):
        self.main_window.save_settings()
        sys.exit(0)

    def toggle_engine(self):
        if self.main_window.engine.running:
            self.main_window.engine.stop()
            self.toggle_action.setText("Başlat")
        else:
            self.main_window.engine.start()
            self.toggle_action.setText("Durdur")