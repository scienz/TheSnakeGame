from view import View
from board import Board

def run():
    board = Board()
    board.initBoard()
    
    view = View(board)
    view.run()
if __name__ == "__main__":
    run()