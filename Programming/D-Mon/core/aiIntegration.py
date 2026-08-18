# core/aiIntegration.py
import time
from PyQt6.QtCore import QThread, pyqtSignal

class AIChatWorker(QThread):
    responseReady = pyqtSignal(str)
    
    def __init__(self, userMessage: str):
        super().__init__()
        self.userMessage = userMessage

    def run(self):
        """API 통신 로직. UI 스레드와 분리되어 백그라운드에서 실행됩니다."""
        try:
            # 실제 구현 시 openai.ChatCompletion.create() 등으로 대체
            # Fallback: API 에러나 지연 방지를 위한 Mock Delay
            time.sleep(1.5) 
            mockResponse = f"응! 네가 '{self.userMessage}'라고 했구나. 오늘도 힘내서 같이 성장하자!"
            self.responseReady.emit(mockResponse)
        except Exception as e:
            self.responseReady.emit("앗, 지금은 네트워크 연결이 불안정해서 대답하기 어려워.")