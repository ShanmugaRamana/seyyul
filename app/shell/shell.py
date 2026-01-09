import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
# Import from engine/browser.py
from engine.browser import BrowserEngine

class SeyyulShell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyyul - Education Platform")
        self.resize(1200, 800)

        # Path to icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icons', 'icon.png')
        self.setWindowIcon(QIcon(icon_path))

        # Initialize the specialized engine
        self.browser = BrowserEngine()
        self.setCentralWidget(self.browser)

def start_shell():
    app = QApplication(sys.argv)
    window = SeyyulShell()
    window.show()
    sys.exit(app.exec())