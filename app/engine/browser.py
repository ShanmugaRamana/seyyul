from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt6.QtCore import QStandardPaths
import os

class BrowserEngine(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 1. Define storage path explicitly
        data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        storage_path = os.path.join(data_path, "SeyyulBrowserData")
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)
            
        print(f"Browser Storage Path: {storage_path}")

        # 2. Create a specific named profile (ensures isolation and persistence)
        # Note: We use a specific string identifier for the profile
        self.profile = QWebEngineProfile("SeyyulProfile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setCachePath(storage_path)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        # 3. Set User Agent
        chrome_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        self.profile.setHttpUserAgent(chrome_user_agent)

        # 4. Configure settings on the profile
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        
        # 5. Create a Page with this profile and set it to the View
        self.web_page = QWebEnginePage(self.profile, self)
        self.setPage(self.web_page)
        
    def navigate(self, url_obj):
        """
        Navigates to the provided QUrl (local or remote).
        """
        self.setUrl(url_obj)