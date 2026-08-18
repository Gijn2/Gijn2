# ui/components/ContentWidget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.btnDispatch = QPushButton("파견 보내기 (EXP 보너스)")
        self.btnHunt = QPushButton("토벌전 입장 (스탯 보너스)")
        self.btnShop = QPushButton("상점")
        
        self.layout.addWidget(self.btnDispatch)
        self.layout.addWidget(self.btnHunt)
        self.layout.addWidget(self.btnShop)
        self.layout.addStretch()