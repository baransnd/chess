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