import pygame
from ChessLogic import GameState

IMAGES = {}
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE / 8

def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    gs = GameState()

    load_pieces()
    running = True
    while (running):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        draw_board(screen)
        draw_pieces(screen, gs.board)
        pygame.display.flip()


    

    """
    creates a board of 8x8 with the correct colors
    """

def draw_board(screen):
    for row in range(8):
        for column in range(8):
            if ((row + column) % 2) == 0:
                color = (139,69,19) 
            else:                    color = (255,230,250)
            pygame.draw.rect(screen, color, (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece == "--":
                continue
            else:
                screen.blit(IMAGES[piece], pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    """
    loads the pieces to a global list called IMAGES
    """
def load_pieces():
    pieces = ['white-pawn','white-rook','white-knight','white-bishop','white-king','white-queen',
              'black-pawn','black-rook','black-knight','black-bishop','black-king','black-queen']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("assets/pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


        
if __name__ == "__main__":
    main()

            
def add:
    

