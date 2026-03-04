import pygame
from constants import *
from states import MenuState, PlayingState
from utils import loadHighscoreSecure

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # 상태 머신 초기화
    currentState = MenuState()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: running = False
            
            # 수익화: 스팀 결제 API 호출 예시 (요청 사항 8번)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print("Steam IAP 결제창 호출...") 

        # 상태 전환 관리
        nextState = currentState.handleEvents(events)
        if nextState: currentState = nextState

        currentState.update()
        currentState.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()