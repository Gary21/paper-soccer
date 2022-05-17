import pygame.event
from Player import Player


class Human(Player):
    def __init__(self, board):
        super().__init__(board)

    def next_move(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        return 0b100000000
                    elif event.key == pygame.K_x:
                        return 0b010000000
                    elif event.key == pygame.K_z:
                        return 0b001000000
                    elif event.key == pygame.K_d:
                        return 0b000100000
                    elif event.key == pygame.K_a:
                        return 0b000001000
                    elif event.key == pygame.K_e:
                        return 0b000000100
                    elif event.key == pygame.K_w:
                        return 0b000000010
                    elif event.key == pygame.K_q:
                        return 0b000000001
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
