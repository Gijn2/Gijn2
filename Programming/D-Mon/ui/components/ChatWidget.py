# ui/components/ChatWidget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from core.aiIntegration import AIChatWorker

class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.chatLog = QTextEdit()
        self.chatLog.setReadOnly(True)
        
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("파트너에게 말 걸기...")
        self.inputField.returnPressed.connect(self.handleSend)
        
        self.btnSend = QPushButton("전송")
        self.btnSend.clicked.connect(self.handleSend)
        
        self.layout.addWidget(self.chatLog)
        self.layout.addWidget(self.inputField)
        self.layout.addWidget(self.btnSend)
        
        self.worker = None

    def handleSend(self):
        message = self.inputField.text().strip()
        if not message: return
        
        self.chatLog.append(f"<b>User:</b> {message}")
        self.inputField.clear()
        self.inputField.setEnabled(False)
        self.btnSend.setEnabled(False)
        
        # 비동기 스레드 실행
        self.worker = AIChatWorker(message)
        self.worker.responseReady.connect(self.handleResponse)
        self.worker.start()

    def handleResponse(self, response: str):
        self.chatLog.append(f"<b>Partner:</b> {response}")
        self.inputField.setEnabled(True)
        self.btnSend.setEnabled(True)