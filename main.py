from Board import *
from Game import Game


def draw_window(win, board):
    win.fill((60, 165, 0))
    board.draw(win)
    pygame.display.update()


if __name__ == '__main__':
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    board = Board()
    game = Game(board)
    pygame.display.set_caption("Papier pilka")

    while True:
        clock.tick(30)
        draw_window(win, board)
        game.handle_moves()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
