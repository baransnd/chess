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
        self.board[end_row][end_column] = self.board[start_row][start_column]
        self.board[start_row][start_column] ="--"
        