from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

class SuggestionPopup(QWidget):
    shortcut_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setFixedWidth(220)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)

    def update_suggestions(self, suggestions):
        self.list_widget.clear()
        if not suggestions:
            self.hide()
            return

        for sc, rep in suggestions:
            item = QListWidgetItem(f"{sc:<12} → {rep.splitlines()[0][:12]}")
            item.setData(Qt.UserRole, sc)
            self.list_widget.addItem(item)
        
        h = min(len(suggestions) * 25 + 10, 130)
        self.setFixedHeight(h)
        
        pos = QCursor.pos()
        self.move(pos.x() + 10, pos.y() + 15)
        self.show()

    def on_item_clicked(self, item):
        sc = item.data(Qt.UserRole)
        self.shortcut_selected.emit(sc)
        self.hide()