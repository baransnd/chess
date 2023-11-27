#ChessLogic.py

class GameState():
    def __init__(self):
        self.board = [["black-rook", "black-knight","black-bishop","black-queen","black-king","black-bishop", "black-knight","black-rook"],
                      ["black-pawn","black-pawn","black-pawn","black-pawn","black-pawn","black-pawn","black-pawn","black-pawn"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["white-pawn","white-pawn","white-pawn","white-pawn","white-pawn","white-pawn","white-pawn","white-pawn"],
                      ["white-rook", "white-knight","white-bishop","white-queen","white-king","white-bishop", "white-knight","white-rook"]]
        self.white_to_move = True
        self.moveLog = []
    
    """
    Moves a piece if it is allowed by chess rules, and changes the turn.
    """    
    def move_piece(self, start, end):
        start_row, start_column = start
        end_row, end_column = end
        piece = self.board[start_row][start_column]

        # Generate all possible moves for the current color
        all_moves = self.generate_moves("white" if self.white_to_move else "black")

        # Check if the move is in the list of possible moves
        if ((start_row, start_column), (end_row, end_column), self.board[end_row][end_column]) in all_moves:
            if (self.is_check_after_move(start, end)):
                print("Invalid move, king in check")
                return False
            else:
                self.move(start, end)
                return True
        else:
            print("Invalid move")
            return False
            
    def move(self, start, end):
        start_row, start_column = start
        end_row, end_column = end
        piece = self.board[start_row][start_column]
        
        # Make the move
        self.board[end_row][end_column] = piece
        self.board[start_row][start_column] = "--"
        self.white_to_move = not self.white_to_move
            
    def check_for_promotion(self, piece, end_row):   
           return ("pawn" in piece) and (end_row == 0 and piece.startswith("white")) or (end_row == 7 and piece.startswith("black"))
       
    def promote_pawn(self, end, piece):
        row, col = end
        color = "black" if self.white_to_move else "white"
        promoted_piece = f"{color}-{piece}"
        self.board[row][col] = promoted_piece
            
        
            
    def is_check_after_move(self, start, end):
        # Simulate the move on the current game state
        piece = self.board[start[0]][start[1]]
        target_piece = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = "--"

        # Check if the opponent can capture the king in the next move
        opponent_color = "black" if self.white_to_move else "white"
        opponent_moves = self.generate_moves(opponent_color)

        # Revert the simulated move
        self.board[start[0]][start[1]] = piece
        self.board[end[0]][end[1]] = target_piece

        for move in opponent_moves:
            print(move)
            if "king" in move[2]:
                return True

        return False
    
    
    
    def generate_moves(self, color):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece != "--" and piece.startswith(color):
                    if "-rook" in piece:
                        moves.extend(self.generate_rook_moves((row, col), color))
                    elif "-knight" in piece:
                        moves.extend(self.generate_knight_moves((row, col), color))
                    elif "-bishop" in piece:
                        moves.extend(self.generate_bishop_moves((row, col), color))
                    elif "-queen" in piece:
                        moves.extend(self.generate_queen_moves((row, col), color))
                    elif "-king" in piece:
                        moves.extend(self.generate_king_moves((row, col), color))
                    elif "-pawn" in piece:
                        moves.extend(self.generate_pawn_moves((row, col), color))

        return moves
    
    
    def generate_pawn_moves(self, start, color):
        moves = []
        start_row, start_column = start

        # Determine the direction of pawn movement based on its color
        direction = -1 if color == "white" else 1

        # Pawn moves one square straight forward
        row = start_row + direction
        if 0 <= row < 8 and self.board[row][start_column] == "--":
            moves.append(((start_row, start_column), (row, start_column), self.board[row][start_column]))

        # Pawn takes diagonally forwards to a neighboring square
        for col_offset in [-1, 1]:
            col = start_column + col_offset
            row = start_row + direction
            if 0 <= row < 8 and 0 <= col < 8:
                target_piece = self.board[row][col]
                if target_piece != "--" and not target_piece.startswith(color):
                    moves.append(((start_row, start_column), (row, col), target_piece))

        # Exception: Pawn can take two steps forward from the starting position
        row = start_row + 2 * direction
        if (
            direction == -1 and start_row == 6 and self.board[row][start_column] == "--" and
            self.board[start_row + direction][start_column] == "--"
        ) or (
            direction == 1 and start_row == 1 and self.board[row][start_column] == "--" and
            self.board[start_row + direction][start_column] == "--"
        ):
            moves.append(((start_row, start_column), (row, start_column), self.board[row][start_column]))

        return moves
    
    """
    A move is not valid, if it ends on  a piece of same color
    """
    def generate_rook_moves(self, start, color):
        moves = []
        start_row, start_column = start

        # Rook moves vertically
        for row in range(start_row + 1, 8):
            moves.append(((start_row, start_column), (row, start_column), self.board[row][start_column]))
            if self.board[row][start_column] != "--":
                if self.board[row][start_column].startswith(color):
                    moves.pop()  # Remove the move with the piece of the same color
                    break  
                else:
                    # Stop adding moves if there's a piece of the same color in the way
                    break

        for row in range(start_row - 1, -1, -1):
            moves.append(((start_row, start_column), (row, start_column), self.board[row][start_column]))
            if self.board[row][start_column] != "--":
                if self.board[row][start_column].startswith(color):
                    moves.pop()  # Remove the move with the piece of the same color
                    break  
                else:
                    # Stop adding moves if there's a piece of the same color in the way
                    break

        # Rook moves horizontally
        for col in range(start_column + 1, 8):
            moves.append(((start_row, start_column), (start_row, col), self.board[start_row][col]))
            if self.board[start_row][col] != "--":
                if self.board[start_row][col].startswith(color):
                    moves.pop()  # Remove the move with the piece of the same color
                    break  
                else:
                    # Stop adding moves if there's a piece of the same color in the way
                    break

        for col in range(start_column - 1, -1, -1):
            moves.append(((start_row, start_column), (start_row, col), self.board[start_row][col]))
            if self.board[start_row][col] != "--":
                if self.board[start_row][col].startswith(color):
                    moves.pop()  # Remove the move with the piece of the same color
                    break  
                else:
                    break

        return moves
    
    def generate_bishop_moves(self, start, color):
        moves = []
        start_row, start_column = start

        # Bishop moves diagonally
        for step_row, step_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            row, col = start_row + step_row, start_column + step_col
            while 0 <= row < 8 and 0 <= col < 8:
                moves.append(((start_row, start_column), (row, col), self.board[row][col]))
                if self.board[row][col] != "--":
                    if self.board[row][col].startswith(color):
                        moves.pop()  # Remove the move with the piece of the same color
                        break  
                    else:
                        # Stop adding moves if there's a piece of diffrent color in the way
                        break
                row += step_row
                col += step_col

        return moves
    
    
    def generate_knight_moves(self, start, color):
        moves = []
        start_row, start_column = start
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for move in knight_moves:
            row, col = start_row + move[0], start_column + move[1]
            if 0 <= row < 8 and 0 <= col < 8:
                target_piece = self.board[row][col]
                if target_piece == "--" or not target_piece.startswith(color):
                    moves.append(((start_row, start_column), (row, col), target_piece))

        return moves
    
    def generate_queen_moves(self, start, color):
        rook_moves = self.generate_rook_moves(start, color)
        bishop_moves = self.generate_bishop_moves(start, color)
        return rook_moves + bishop_moves
    
    def generate_king_moves(self, start, color):
        moves = []
        start_row, start_column = start

        # King moves one square in any direction
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                row, col = start_row + row_offset, start_column + col_offset
                if 0 <= row < 8 and 0 <= col < 8:
                    target_piece = self.board[row][col]
                    if target_piece == "--" or not target_piece.startswith(color):
                        moves.append(((start_row, start_column), (row, col), target_piece))

        return moves