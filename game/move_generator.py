from game.pieces import King
from copy import deepcopy

class MoveGenerator():
    def __init__(self, board):
        self.board = board

    def get_legal_moves(self):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece.color == self.board.turn:
                    if len(self.board.move_log) == 0:
                        last_move = None 
                    else:
                        last_move = self.board.move_log[-1]
                    valid_moves = piece.get_valid_moves(self.board, last_move)
                    for move in valid_moves:
                        if self.is_move_legal(piece, move):
                            legal_moves.append((piece.position, move))
        return legal_moves
    
    def is_move_legal(self, piece, move):
        x_old, y_old = piece.position
        x_new, y_new = move
        if not (0 <= x_new < 8 and 0 <= y_new < 8):
            return False
        valid_moves = piece.get_valid_moves(self.board)
        if (x_new, y_new) not in valid_moves:
            return False
        temp_board = deepcopy(self.board)
        # Di chuyển quân cờ trên bản sao
        moving_piece = temp_board.board[x_old][y_old]
        temp_board.board[x_new][y_new] = moving_piece
        temp_board.board[x_old][y_old] = None
        if moving_piece:
            moving_piece.position = (x_new, y_new)
        in_check_after_move = temp_board.is_in_check(temp_board.turn)
        return not in_check_after_move
    