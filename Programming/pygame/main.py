import pygame
from constants import WIDTH, HEIGHT, FPS
from states import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Topdown Shooting: Modular Edition")
    clock = pygame.time.Clock()

    # 데이터 컨텍스트 생성 및 초기 상태 진입
    ctx = GameContext()
    currentState = PlayingState(ctx)
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # 1. 상태 전이 확인
        nextState = currentState.handleEvents(events)
        if nextState:
            currentState = nextState

        # 2. 로직 업데이트
        transitionalState = currentState.update()
        if transitionalState:
            currentState = transitionalState

        # 3. 화면 렌더링
        screen.fill((10, 10, 15)) # 배경색
        currentState.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()