from board import Board
from pieces import King  # Import King để kiểm tra isinstance
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
                    valid_moves = piece.get_valid_moves(self.board, self.board.move_log[-1])
                    for move in valid_moves:
                        if self.is_move_legal(piece, move):
                            legal_moves.append((piece.position, move))
        return legal_moves
    
    def is_move_legal(self, piece, move):
        x_old, y_old = piece.position
        x_new, y_new = move

        # Kiểm tra nước đi có trong bàn cờ không
        if not (0 <= x_new < 8 and 0 <= y_new < 8):
            return False

        temp_board = deepcopy(self.board)  # Sao chép sâu (tùy chọn)
        temp_board.board[x_new][y_new] = temp_board.board[x_old][y_old]
        temp_board.board[x_old][y_old] = None

        # Lưu vị trí cũ và cập nhật tạm thời nếu là vua
        old_position = piece.position[:]
        piece.position = [x_new, y_new]

        # Kiểm tra chiếu
        in_check = self.is_in_check(temp_board, self.board.turn)

        # Khôi phục vị trí
        piece.position = old_position

        return not in_check
    
    def is_in_check(self, board: Board, color):
        # Tìm vị trí của vua
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break
        
        if not king_position:
            raise ValueError(f"Không tìm thấy vua của {color} trên bàn cờ!")
    
        # Kiểm tra xem có quân nào có thể ăn vua không
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.color != color:
                    valid_moves = piece.get_valid_moves(board)
                    if king_position in valid_moves:
                        return True
        return False