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
        
        # Tạo bản sao sâu của bàn cờ và quân cờ
        temp_board = deepcopy(self.board)
        
        # QUAN TRỌNG: Lấy quân cờ từ bàn cờ đã sao chép, không dùng quân cờ gốc
        moving_piece = temp_board.board[x_old][y_old]
        
        # Di chuyển quân cờ trên bản sao
        moving_piece.move((x_new, y_new), temp_board)
        
        # Debug: Kiểm tra xem vua có trên bàn cờ không
        king_found = False
        for row in range(8):
            for col in range(8):
                if isinstance(temp_board.board[row][col], King) and temp_board.board[row][col].color == temp_board.turn:
                    king_found = True
                    break
            if king_found:
                break
        if not king_found:
            print("Debug: Trạng thái temp_board khi không tìm thấy vua:")
            print(temp_board)
            raise ValueError(f"Không tìm thấy vua của {temp_board.turn} trong temp_board!")
        
        in_check_after_move = temp_board.is_in_check(temp_board.turn)
        return not in_check_after_move
        