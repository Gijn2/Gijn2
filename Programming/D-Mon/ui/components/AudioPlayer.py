# ui/components/AudioPlayer.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class AudioPlayer(QWidget):
    def __init__(self, defaultVideoId: str = "jfKfPfyJRdk"): # Lofi Girl 기본값
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.webView = QWebEngineView()
        self.layout.addWidget(self.webView)
        
        self.loadYoutubeStream(defaultVideoId)

    def loadYoutubeStream(self, videoId: str):
        """유튜브 임베드 URL을 로드합니다. 플레이리스트/반복재생 파라미터 적용."""
        try:
            urlStr = f"https://www.youtube.com/embed/{videoId}?autoplay=1&loop=1&playlist={videoId}"
            self.webView.setUrl(QUrl(urlStr))
        except Exception as e:
            print(f"Failed to load Youtube stream. Error: {e}")