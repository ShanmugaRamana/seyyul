from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings

class BrowserEngine(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configure browser settings for the hybrid environment
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)

    def navigate(self, url_obj):
        """
        Navigates to the provided QUrl (local or remote).
        """
        self.setUrl(url_obj)