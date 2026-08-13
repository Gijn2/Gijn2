# ui/MainWindow.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt6.QtCore import QTimer
from core.saveLoadManager import SaveLoadManager
from core.idleCalculator import IdleCalculator
from ui.components.AudioPlayer import AudioPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digi-Idle: Lofi Study Room")
        self.resize(1024, 768)
        
        # State Initialization
        self.saveManager = SaveLoadManager()
        self.gameState = self.saveManager.loadData()
        
        # UI & Timer Setup
        self._initUI()
        self._initTimers()

    def _initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QHBoxLayout(centralWidget)
        
        # 1. Left Layout (Lofi Player & System)
        leftLayout = QVBoxLayout()
        self.audioPlayer = AudioPlayer()
        leftLayout.addWidget(self.audioPlayer, stretch=1)
        
        self.btnSettings = QPushButton("System Settings")
        leftLayout.addWidget(self.btnSettings)
        
        # 2. Center Layout (Character Canvas)
        centerLayout = QVBoxLayout()
        self.lblCharacter = QLabel(f"Partner: {self.gameState['partnerName']}")
        self.lblCharacter.setStyleSheet("font-size: 24px; font-weight: bold;")
        centerLayout.addWidget(self.lblCharacter)
        centerLayout.addStretch()
        
        # 3. Right Layout (Status & Content)
        rightLayout = QVBoxLayout()
        self.btnTraining = QPushButton("Dispatch / Hunt (Content)")
        
        # Status Sub-widget
        self.statusWidget = QWidget()
        statusLayout = QVBoxLayout(self.statusWidget)
        self.lblLevel = QLabel(f"Level: {self.gameState['level']}")
        self.expBar = QProgressBar()
        self.expBar.setMaximum(100) # 렌더링용 임시 Max (Tick에서 비율로 계산)
        statusLayout.addWidget(self.lblLevel)
        statusLayout.addWidget(self.expBar)
        
        self.btnToggleStatus = QPushButton("Toggle Status Window")
        self.btnToggleStatus.clicked.connect(self.handleToggleStatus)
        
        rightLayout.addWidget(self.btnTraining)
        rightLayout.addStretch()
        rightLayout.addWidget(self.statusWidget)
        rightLayout.addWidget(self.btnToggleStatus)
        
        mainLayout.addLayout(leftLayout, stretch=2)
        mainLayout.addLayout(centerLayout, stretch=3)
        mainLayout.addLayout(rightLayout, stretch=2)

    def _initTimers(self):
        self.idleTimer = QTimer(self)
        self.idleTimer.timeout.connect(self.handleIdleTick)
        self.idleTimer.start(1000) # 1초 틱

    def handleIdleTick(self):
        """1초마다 실행되는 핵심 루프: 로직 연산 후 UI에 반영합니다."""
        try:
            # 1. Logic Calculation
            gainedExp = IdleCalculator.calculateTickExp(2.0, self.gameState["buffMultiplier"])
            self.gameState["currentExp"] += gainedExp
            
            isLevelUp, newLevel, remExp = IdleCalculator.checkLevelUp(
                self.gameState["currentExp"], 
                self.gameState["level"]
            )
            
            # 2. State Update
            if isLevelUp:
                self.gameState["level"] = newLevel
                self.gameState["currentExp"] = remExp
                self.lblLevel.setText(f"Level: {self.gameState['level']}")
            
            # 3. UI Render Update
            reqExp = 100.0 * (self.gameState["level"] ** 1.5)
            expPercentage = int((self.gameState["currentExp"] / reqExp) * 100)
            self.expBar.setValue(expPercentage)
            
        except Exception as e:
            print(f"Error during idle tick: {e}")

    def handleToggleStatus(self):
        isVisible = self.statusWidget.isVisible()
        self.statusWidget.setVisible(not isVisible)

    def closeEvent(self, event):
        """창 종료 시 안전하게 데이터를 저장합니다."""
        self.saveManager.saveData(self.gameState)
        event.accept()