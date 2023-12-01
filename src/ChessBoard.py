#ChessBoard.py

import pygame
from ChessLogic import GameState

IMAGES = {}
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE / 8
MAX_FPS = 10

dragging_piece = None
drag_start = None
running = True

"""
Entry point of the program. Here the chess board and gamestate are initalized.
The use input is handled, and the board is updated continously until the game ends,
through the exit button or ending of the chess game (mate or stalemate).
"""        
def main():
    global running
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    gs = GameState()
    load_pieces()
    
    while (running):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_down(e, gs)
            elif e.type == pygame.MOUSEBUTTONUP:
                handle_mouse_up(e,gs, screen)
                    
        draw_board(screen)
        draw_pieces(screen, gs.board)
        
        clock.tick(MAX_FPS)
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
    pygame.draw.rect(screen, (50, 10, 10), (0, 0, BOARD_SIZE, BOARD_SIZE), 6)

"draws the pieces on the board in accordance to their position in the game state"
def draw_pieces(screen, board):
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            # no need to draw if the square is empty
            if piece != "--":
                    screen.blit(IMAGES[piece], pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

"""
loads the pieces to a global list called IMAGES
"""
def load_pieces():
    pieces = ['white-pawn','white-rook','white-knight','white-bishop','white-king','white-queen',
              'black-pawn','black-rook','black-knight','black-bishop','black-king','black-queen']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("assets/pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

"""
saves the selected piece and its starting position to grobal variables as the player selects a piece with the mouse
"""
def handle_mouse_down(event, gs):
    global dragging_piece, drag_start
    if event.button == 1:  # Left mouse button
        col = int(event.pos[0] // SQUARE_SIZE)
        row = int(event.pos[1] // SQUARE_SIZE)
        dragging_piece = gs.board[row][col]
        drag_start = (row, col)
"""
tries to make the given move by giving the requested piece movement to the gamestate. Finishes the game when necessary
"""
def handle_mouse_up(event, gs, screen):
    global dragging_piece, drag_start, running
    if event.button == 1 and dragging_piece != "--":
        col = int(event.pos[0] // SQUARE_SIZE)
        row = int(event.pos[1] // SQUARE_SIZE)
        if col < 0 or col > 7 or row > 7 or row < 0:
            return
        end_position = (row, col)
        if gs.move_piece(drag_start, end_position):
            if gs.check_for_promotion(end_position):
                handle_promotion(screen, gs,end_position)
            if gs.is_checkmate():
                font = pygame.font.Font(None, 74)
                if gs.is_stalemate():
                    text = font.render("Tie", True, (255, 0, 0))
                else:
                    text = font.render("Game Over", True, (255, 0, 0))
                text_rect = text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

        dragging_piece = None
        drag_start = None  # Reset drag_start after the move

"""
Creates a promotion screen from which the player can select the piece to promote to
"""
def handle_promotion(screen, gs, end):
    promotion_options = ["queen", "rook", "bishop", "knight"]
    font = pygame.font.Font(None, 36)
    
    instruction_lines = ["Choose a promotion piece:"]
    for option in promotion_options:
        instruction_lines.append(f"Press {option[0]} for {option.capitalize()}")

    text_height = sum([font.get_linesize() for _ in instruction_lines])
    y_position = (BOARD_SIZE - text_height) // 2

    screen.fill((139,69,19))

    for line in instruction_lines:
        text = font.render(line, True, (255, 255, 255))
        rect = text.get_rect(center=(BOARD_SIZE // 2, y_position))
        screen.blit(text, rect)
        y_position += font.get_linesize()

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i, option in enumerate(promotion_options):
                    if event.key == getattr(pygame, f"K_{option[0]}"):
                        chosen_option = option
                        gs.promote_pawn(end, chosen_option)
                        return chosen_option
        
if __name__ == "__main__":
    main()
    


