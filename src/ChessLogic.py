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
        
        if (self.check_move(piece,start,end)):
            if self.board[end_row][end_column] == "--":
                self.board[end_row][end_column] = self.board[start_row][start_column]
                self.board[start_row][start_column] = "--"
                self.white_to_move = not self.white_to_move
            elif(self.check_capture(piece, end)):
                print(start, end)
                self.board[end_row][end_column] = self.board[start_row][start_column]
                self.board[start_row][start_column] ="--"
                self.white_to_move = not self.white_to_move
            else:
                print("can not capture own piece")
        else:
            print("impossible move")
            pass
        
    """
    Checks if the captured piece is not of the same color.
    """    
    def check_capture(self, piece,end):
        end_row, end_column = end
        captured = self.board[end_row][end_column]
        if "white" in piece:
            if "white" in captured:
                return False
        else:
            if "black" in captured:
                return False
        return True
    
    """
    Checks if a piece movement is valid without considering checks
    """    
    def check_move(self, piece, start, end):
        #check the turn of play
        if (self.white_to_move == True):
            if "black" in piece:
                return False
        else:
            if "white" in piece:
                return False
                
        start_row, start_column = start
        end_row, end_column = end
        
        #check for out of bounds
        if end_row > 7 or end_row < 0:
            return False
        if end_column > 7 or end_column < 0:
            return False
        
        if "-rook" in piece:
            # Rook moves vertically or horizontally
            return self.check_rook_move(start, end)

        elif "-knight" in piece:
            # Knight moves in an L-shape (2 squares in one direction and 1 square in the other)
            return (abs(start_row - end_row) == 2 and abs(start_column - end_column) == 1) or \
                   (abs(start_row - end_row) == 1 and abs(start_column - end_column) == 2)

        elif "-bishop" in piece:
            # Bishop moves diagonally
            return self.check_bishop_move(start, end)

        elif "-queen" in piece:
            # Queen moves horizontally, vertically, or diagonally
            return self.check_queen_move(start, end)

        elif "-king" in piece:
            # King moves one square in any direction
            return abs(start_row - end_row) <= 1 and abs(start_column - end_column) <= 1

        elif "-pawn" in piece:
            color = "white" if piece.startswith("white") else "black"
            return self.checkPawnMove(start, end, color)

        return True
    
    """
    Checks if a pawn movement is valid without considering checks
    """
    
    def checkPawnMove(self, start, end, color):
        start_row, start_column = start
        end_row, end_column = end

        # Determine the direction of pawn movement based on its color
        direction = -1 if color == "white" else 1

        # Pawn moves one square straight forward
        if start_column == end_column and start_row + direction == end_row and self.board[end_row][end_column] == "--":
            return True

        # Pawn takes diagonally forwards to a neighbouring square
        if abs(start_column - end_column) == 1 and start_row + direction == end_row:
            target_piece = self.board[end_row][end_column]
            return target_piece != "--" and not target_piece.startswith(color)

        # Exception: Pawn can take two steps forward from the starting position
        if start_column == end_column and start_row + 2 * direction == end_row and start_row == 1 and color == "black":
            return self.board[start_row + direction][start_column] == "--"

        if start_column == end_column and start_row + 2 * direction == end_row and start_row == 6 and color == "white":
            return self.board[start_row + direction][start_column] == "--"

        return False
    
    
    """
    Checks if a rook movement is valid without considering checks
    """    
    def check_rook_move(self, start, end):
        start_row, start_column = start
        end_row, end_column = end

        # Rook moves vertically or horizontally
        if start_row == end_row or start_column == end_column:
            # Check for any pieces in the path
            if start_row == end_row:
                # Moving horizontally
                step = 1 if end_column > start_column else -1
                for col in range(start_column + step, end_column, step):
                    if self.board[start_row][col] != "--":
                        return False
            else:
                # Moving vertically
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if self.board[row][start_column] != "--":
                        return False

            return True

        return False
    
    
    """
    Checks if a bishop movement is valid without considering checks
    """
    def check_bishop_move(self, start, end):
        start_row, start_column = start
        end_row, end_column = end

        # Bishop moves diagonally
        if abs(start_row - end_row) == abs(start_column - end_column):
            # Check for any pieces in the diagonal path
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_column > start_column else -1

            row, col = start_row + step_row, start_column + step_col
            while row != end_row and col != end_column:
                if self.board[row][col] != "--":
                    return False
                row += step_row
                col += step_col

            return True

        return False
    
    
    """
    Checks if a queen movement is valid without considering checks
    """    
    def check_queen_move(self, start, end):
        return self.check_bishop_move(start, end) or self.check_rook_move(start,end)
    
    
    
    
    #new stuff
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