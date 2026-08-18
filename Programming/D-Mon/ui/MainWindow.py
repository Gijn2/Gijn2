# ui/MainWindow.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QTimer
from core.saveLoadManager import SaveLoadManager
from core.idleCalculator import IdleCalculator
from ui.components.AudioPlayer import AudioPlayer
from ui.components.StatusWidget import StatusWidget
from ui.components.CharacterCanvas import CharacterCanvas
from ui.components.ContentWidget import ContentWidget
from ui.components.ChatWidget import ChatWidget
from utils.constants import TICK_INTERVAL_MS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digi-Idle: Lofi Study Room")
        self.resize(1024, 768)
        
        self.saveManager = SaveLoadManager()
        self.gameState = self.saveManager.loadData()
        
        self._initUI()
        self._initTimers()

    def _initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QHBoxLayout(centralWidget)
        
        # 1. Left Layout (Audio & Chat)
        leftLayout = QVBoxLayout()
        self.audioPlayer = AudioPlayer()
        self.chatWidget = ChatWidget()
        leftLayout.addWidget(self.audioPlayer, stretch=1)
        leftLayout.addWidget(self.chatWidget, stretch=1)
        
        # 2. Center Layout (Character Animation)
        centerLayout = QVBoxLayout()
        self.characterCanvas = CharacterCanvas(self.gameState["partnerName"])
        centerLayout.addWidget(self.characterCanvas)
        
        # 3. Right Layout (Status & Content)
        rightLayout = QVBoxLayout()
        self.contentWidget = ContentWidget()
        self.statusWidget = StatusWidget()
        rightLayout.addWidget(self.contentWidget, stretch=1)
        rightLayout.addWidget(self.statusWidget, stretch=1)
        
        mainLayout.addLayout(leftLayout, stretch=2)
        mainLayout.addLayout(centerLayout, stretch=3)
        mainLayout.addLayout(rightLayout, stretch=2)
        
        # Initial UI Sync
        self.statusWidget.updateStatus(self.gameState)

    def _initTimers(self):
        self.idleTimer = QTimer(self)
        self.idleTimer.timeout.connect(self.handleIdleTick)
        self.idleTimer.start(TICK_INTERVAL_MS)

    def handleIdleTick(self):
        try:
            gainedExp = IdleCalculator.calculateTickExp(2.0, self.gameState.get("buffMultiplier", 1.0))
            self.gameState["currentExp"] += gainedExp
            
            isLevelUp, newLevel, remExp = IdleCalculator.checkLevelUp(
                self.gameState["currentExp"], 
                self.gameState["level"]
            )
            
            if isLevelUp:
                self.gameState["level"] = newLevel
                self.gameState["currentExp"] = remExp
            
            # UI 일괄 업데이트 (단방향 데이터 플로우)
            self.statusWidget.updateStatus(self.gameState)
            
        except Exception as e:
            print(f"Error during idle tick: {e}")

    def closeEvent(self, event):
        self.saveManager.saveData(self.gameState)
        event.accept()