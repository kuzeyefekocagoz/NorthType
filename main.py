import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from keyboard_engine import KeyboardEngine

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    engine = KeyboardEngine()
    engine.start()

    window = MainWindow(engine)
    window.show()
    
    exit_code = app.exec()
    
    engine.stop()
    sys.exit(exit_code)