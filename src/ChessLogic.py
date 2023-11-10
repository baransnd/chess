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
        if (self.checkMove(piece,start,end)):
            if self.board[end_row][end_column] == "--":
                self.board[end_row][end_column] = self.board[start_row][start_column]
                self.board[start_row][start_column] ="--"
            else:
                pass
        else:
            print("impossible move")
            pass
        
    def checkMove(self, piece, start, end):
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
            # Pawn moves forward one square, but captures diagonally
            if "white" in piece:
                return (end_row == start_row - 1 and end_column == start_column) or \
                       (end_row == start_row - 1 and abs(end_column - start_column) == 1 and self.board[end_row][end_column] != "--")
            elif "black" in piece:
                return (end_row == start_row + 1 and end_column == start_column) or \
                       (end_row == start_row + 1 and abs(end_column - start_column) == 1 and self.board[end_row][end_column] != "--")

        return True
        