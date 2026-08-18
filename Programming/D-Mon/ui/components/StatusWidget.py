# ui/components/StatusWidget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton
from utils.constants import BASE_REQ_EXP

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.lblName = QLabel("Name: Unknown")
        self.lblLevel = QLabel("Level: 1")
        self.expBar = QProgressBar()
        self.expBar.setMaximum(100)
        
        self.btnEvolution = QPushButton("진화 / 퇴화")
        
        self.layout.addWidget(self.lblName)
        self.layout.addWidget(self.lblLevel)
        self.layout.addWidget(self.expBar)
        self.layout.addWidget(self.btnEvolution)
        self.layout.addStretch()

    def updateStatus(self, gameState: dict):
        """데이터를 전달받아 UI를 갱신합니다."""
        self.lblName.setText(f"Name: {gameState.get('partnerName', 'Unknown')}")
        self.lblLevel.setText(f"Level: {gameState.get('level', 1)}")
        
        currentLevel = gameState.get("level", 1)
        currentExp = gameState.get("currentExp", 0)
        reqExp = BASE_REQ_EXP * (currentLevel ** 1.5)
        
        expPercentage = int((currentExp / reqExp) * 100) if reqExp > 0 else 0
        self.expBar.setValue(min(expPercentage, 100))