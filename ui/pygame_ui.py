import pygame
import sys

class PygameUI:
    def __init__(self, board):
        pygame.init()
        self.board = board
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Chess Bot Game")
        self.clock = pygame.time.Clock()

    def draw_board(self):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(col * 75, row * 75, 75, 75))

    def draw_pieces(self):
        # Placeholder for drawing pieces
        pass

    def update(self):
        self.screen.fill(pygame.Color("black"))
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.clock.tick(60)