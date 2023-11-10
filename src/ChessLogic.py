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
        
    def check_move(self, piece, start, end):
        if (self.white_to_move == True):
            if "black" in piece:
                return False
        else:
            if "white" in piece:
                return False
                
        start_row, start_column = start
        end_row, end_column = end
        
        if "-rook" in piece:
            # Rook moves vertically or horizontally
            return start_row == end_row or start_column == end_column

        elif "-knight" in piece:
            # Knight moves in an L-shape (2 squares in one direction and 1 square in the other)
            return (abs(start_row - end_row) == 2 and abs(start_column - end_column) == 1) or \
                   (abs(start_row - end_row) == 1 and abs(start_column - end_column) == 2)

        elif "-bishop" in piece:
            # Bishop moves diagonally
            return abs(start_row - end_row) == abs(start_column - end_column)

        elif "-queen" in piece:
            # Queen moves horizontally, vertically, or diagonally
            return start_row == end_row or start_column == end_column or abs(start_row - end_row) == abs(start_column - end_column)

        elif "-king" in piece:
            # King moves one square in any direction
            return abs(start_row - end_row) <= 1 and abs(start_column - end_column) <= 1

        elif "-pawn" in piece:
            color = "white" if piece.startswith("white") else "black"
            return self.checkPawnMove(start, end, color)

        return True
    
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
        