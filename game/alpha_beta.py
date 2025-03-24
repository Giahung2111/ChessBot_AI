from board import Board
from copy import deepcopy
from evaluator import evaluate_board # Hàm đánh giá trả về giá trị càng lớn càng tốt
import math

# Quy trình hoạt động:
# 1. Duyệt tất cả các nước đi có thể thực hiện (board.get_legal_moves()).
# 2. Mô phỏng trạng thái mới sau khi đi quân bằng board.generate_state_from_a_move(move).
# 3. Gọi minimax để tính giá trị nước đi đó.
# 4. Nếu giá trị này lớn hơn giá trị tốt nhất trước đó, cập nhật best_move và best_value.
# 5. Cập nhật alpha để tối ưu cắt tỉa Alpha-Beta.

class AlphaBeta():
    def __init__(self, depth):
        self.depth = depth

    # Hàm tìm nước đi tốt nhất cho người chơi hiện tại
    def find_best_move(self, board: Board):
        best_move = None
        best_value = -math.inf # Âm vô cực
        alpha = -math.inf
        beta = math.inf # Dương vô cực

        for move in board.get_legal_moves():
            temp_board = board.generate_state_from_a_move(move)
            board_value = self.minimax(temp_board, self.depth - 1, alpha, beta, False)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            alpha = max(alpha, board_value)
        return best_move, best_value

    # Thuật toán Minimax với Alpha-Beta Pruning
    def minimax(self, board: Board, depth, alpha, beta, is_bot_turn):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate_board(board)
        
        if is_bot_turn: # Lượt của bot: Tối đa hóa điểm số
            max_eval = -math.inf
            for move in board.get_legal_moves():
                temp_board = board.generate_state_from_a_move(move)
                eval = self.minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break # Cắt tỉa alpha-beta
            return max_eval
        else: # Lượt của đối thủ: Tối thiểu hóa điểm số
            min_eval = math.inf
            for move in board.get_legal_moves():
                temp_board = board.generate_state_from_a_move(move)
                eval = self.minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break # Cắt tỉa alpha-beta
            return min_eval
        
    # Nếu lấy giá trị càng nhỏ càng tốt cho bot
    # if is_bot_turn:
    #     min_eval = math.inf  # Đổi max -> min
    #     for move in board.get_legal_moves():
    #         temp_board = board.generate_state_from_a_move(move)
    #         eval = self.minimax(temp_board, depth - 1, alpha, beta, False)
    #         min_eval = min(min_eval, eval)  # Đổi max -> min
    #         alpha = min(alpha, eval)  # Đổi max -> min
    #         if beta <= alpha:
    #             break  # Cắt tỉa Alpha-Beta
    #     return min_eval  # Đổi max -> min
    # else:
    #     max_eval = -math.inf  # Đổi min -> max
    #     for move in board.get_legal_moves():
    #         temp_board = board.generate_state_from_a_move(move)
    #         eval = self.minimax(temp_board, depth - 1, alpha, beta, True)
    #         max_eval = max(max_eval, eval)  # Đổi min -> max
    #         beta = max(beta, eval)  # Đổi min -> max
    #         if beta <= alpha:
    #             break  # Cắt tỉa Alpha-Beta
    #     return max_eval  # Đổi min -> max


    # Hàm kiểm tra trạng thái kết thúc
    def is_terminal(self, board: Board):
        return len(board.get_legal_moves()) == 0 # Không còn nước đi hợp lệ