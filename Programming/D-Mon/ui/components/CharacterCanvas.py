# ui/components/CharacterCanvas.py
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt

class CharacterCanvas(QWidget):
    def __init__(self, partnerName: str):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.imageLabel)
        
        self.loadCharacter(partnerName)

    def loadCharacter(self, partnerName: str):
        """이름에 맞는 GIF를 로드합니다. 파일이 없을 시 Fallback(텍스트) 제공."""
        imagePath = f"assets/images/{partnerName.lower()}.gif"
        try:
            self.movie = QMovie(imagePath)
            if not self.movie.isValid():
                raise FileNotFoundError
            self.imageLabel.setMovie(self.movie)
            self.movie.start()
        except Exception:
            self.imageLabel.setText(f"[{partnerName} Pixel Art Missing]")
            self.imageLabel.setStyleSheet("font-size: 20px; color: gray;")