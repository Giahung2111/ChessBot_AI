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

        # Kiểm tra xem nước đi có trong danh sách hợp lệ không
        valid_moves = piece.get_valid_moves(self.board)
        if (x_new, y_new) not in valid_moves:
            return False

        # Tạo bản sao bàn cờ để thử nước đi
        temp_board = deepcopy(self.board)
        temp_board.board[x_new][y_new] = temp_board.board[x_old][y_old]
        temp_board.board[x_old][y_old] = None

        old_position = piece.position
        piece.position = (x_new, y_new)

        # Kiểm tra xem vua của bên hiện tại có còn bị chiếu sau nước đi không
        in_check_after_move = self.is_in_check(temp_board.turn)

        piece.position = old_position

        return not in_check_after_move
    
    def is_in_check(self, color):
        from game.board import Board
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break
        
        if not king_position:
            raise ValueError(f"Không tìm thấy vua của {color} trên bàn cờ!")
    
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece.color != color:
                    valid_moves = piece.get_valid_moves(self.board)
                    if king_position in valid_moves:
                        return True
        return False