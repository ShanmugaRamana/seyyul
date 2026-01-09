import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QUrl
from engine.browser import BrowserEngine

class SeyyulShell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyyul - Education Platform")
        self.resize(1200, 800)

        # Icon setup
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icons', 'icon.png')
        self.setWindowIcon(QIcon(icon_path))

        # Initialize Browser
        self.browser = BrowserEngine()
        
        # Point to the local Node.js server
        # (Ensure you run 'npm start' in app/frontend before running this python script)
        self.browser.navigate(QUrl("http://localhost:3000"))
        
        self.setCentralWidget(self.browser)

def start_shell():
    app = QApplication(sys.argv)
    window = SeyyulShell()
    window.show()
    sys.exit(app.exec())