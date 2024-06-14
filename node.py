class Node:
    def __init__(self, board, dubina, player,move=None):
        self.board = board 
        self.move=move 
        self.dubina = dubina
        self.player = player 
        self.children = [] 
        self.vrednost = 0 
        self.poeni=0