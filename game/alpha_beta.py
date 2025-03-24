from board import Board
from copy import deepcopy
import math
from pieces import King, Knight, Queen, Pawn, Rook, Bishop

# Quy trình hoạt động:
# 1. Duyệt tất cả các nước đi có thể thực hiện (board.get_legal_moves()).
# 2. Mô phỏng trạng thái mới sau khi đi quân bằng board.generate_state_from_a_move(move).
# 3. Gọi minimax để tính giá trị nước đi đó.
# 4. Nếu giá trị này lớn hơn giá trị tốt nhất trước đó, cập nhật best_move và best_value.
# 5. Cập nhật alpha để tối ưu cắt tỉa Alpha-Beta.

class AlphaBeta():
    def __init__(self, depth, bot_color):
        self.depth = depth
        self.bot_color = bot_color

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
    
    def evaluate_board(self, board: Board):
        """
        1. Material (Giá trị vật chất)
            + Pawn: 1 điểm
            + Bishop/Knight: 3 điểm
            + Rook: 5 điểm
            + Queen: 9 điểm
            + King: 1000 điểm

        2. Mobility (Điểm cơ động)
            + 0.05 điểm cho mỗi nước đi hợp lệ

        3. King safety (Điểm an toàn của vua)
            - Số quân bảo vệ vua: Mỗi quân cùng màu có thể di chuyển đến ô xung quanh của vua: +0.05 điểm
            - Mặc định số chốt trước mặt vua là 3, nếu thiếu 1 chốt tương ứng -0.15 điểm

        4. Pawn structure (Cấu trúc tốt)
            - Mỗi tốt thừa (từ tốt thứ 2 trở lên ở cùng cột): -0.1 điểm
            - Tốt thông: Với tốt thông +0.15 điểm, và nếu gần phong cấp thì cộng 0.25 điểm
            - Tốt lạc hậu (là tốt cô lập nhưng thêm việc bị tốt đồng minh chặn): -0.2 điểm
            - Tốt nối liền nhau: +0.1
        """

        # Tính điểm của bot
        material_bot_score = self.evaluate_material_score(board, self.bot_color)
        mobility_bot_score = self.evaluate_mobility_score(board, self.bot_color)
        king_safety_bot_score = self.evaluate_king_safety_score(board, self.bot_color)
        pawn_structure_bot_score = self.evaluate_pawn_structure_score(board, self.bot_color)
        total_bot_score = material_bot_score + mobility_bot_score + king_safety_bot_score + pawn_structure_bot_score

        # Tính điểm cho người chơi (đối thủ của bot)
        player_color = "white" if self.bot_color == "black" else "black"
        material_player_score = self.evaluate_material_score(board, player_color)
        mobility_player_score = self.evaluate_mobility_score(board, player_color)
        king_safety_player_score = self.evaluate_king_safety_score(board, player_color)
        pawn_structure_player_score = self.evaluate_pawn_structure_score(board, player_color)
        total_player_score = material_player_score + mobility_player_score + king_safety_player_score + pawn_structure_player_score

        final_score = total_bot_score - total_player_score
        return final_score

    # 1. Material (Giá trị vật chất)
    def evaluate_material_score(self, board: Board, color):
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board.board[i][j] # Lấy quân cờ ở vị trí hiện tại
                if isinstance(piece, Pawn) and piece.color == color:
                    score += 1
                elif (isinstance(piece, Bishop) and piece.color == color) or (isinstance(piece, Knight) and piece.color == color):
                    score += 3
                elif isinstance(piece, Rook) and piece.color == color:
                    score += 5
                elif isinstance(piece, Queen) and piece.color == color:
                    score += 9
                elif isinstance(piece, King) and piece.color == color:
                    score += 1000 

        return score

    # 2. Mobility (Điểm cơ động)
    def evaluate_mobility_score(self, board: Board, color):
        score = 0
        # Kiểm tra xem board.turn có khớp với color không
        if board.turn == color:
            legal_move_number = len(board.get_legal_moves())
        # Nếu không khớp, cần chuyển lượt tạm thời để lấy nước đi của bên color
        else:
            board.switch_turns()
            legal_move_number = len(board.get_legal_moves())
            board.switch_turns()
        score = legal_move_number * 0.05
        return score

    # 3. King safety (Điểm an toàn của vua)
    def evaluate_king_safety_score(self, board: Board, color):
        """
        Đánh giá an toàn của vua dựa trên:
        - Thiếu chốt chính diện trước mặt vua: -0.2 điểm.
        - Thiếu chốt bên trái/phải trước mặt vua: -0.1 điểm mỗi bên.
        - Mỗi quân cùng màu bảo vệ ô xung quanh vua: +0.05 điểm.
        """
        score = 0

        # 1. Tìm vị trí của vua
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:  # Nếu không tìm thấy vua (trường hợp hiếm)
            return score

        king_row, king_col = king_position

        # 2. Kiểm tra chốt trước mặt vua
        middle_pawn_check = False
        if color == "white" and king_row > 0:  # Vua trắng: kiểm tra hàng trên
            if isinstance(board.board[king_row - 1][king_col], Pawn) and \
               board.board[king_row - 1][king_col].color == color:
                middle_pawn_check = True
        elif color == "black" and king_row < 7:  # Vua đen: kiểm tra hàng dưới
            if isinstance(board.board[king_row + 1][king_col], Pawn) and \
               board.board[king_row + 1][king_col].color == color:
                middle_pawn_check = True
        if not middle_pawn_check:
            score -= 0.2

        # 3. Kiểm tra chốt bên trái và phải trước mặt vua
        left_pawn_check = False
        right_pawn_check = False
        if color == "white" and king_row > 0:  # Vua trắng: hàng trên
            if king_col > 0:  # Kiểm tra biên trái
                if isinstance(board.board[king_row - 1][king_col - 1], Pawn) and \
                   board.board[king_row - 1][king_col - 1].color == color:
                    left_pawn_check = True
            if king_col < 7:  # Kiểm tra biên phải
                if isinstance(board.board[king_row - 1][king_col + 1], Pawn) and \
                   board.board[king_row - 1][king_col + 1].color == color:
                    right_pawn_check = True
        elif color == "black" and king_row < 7:  # Vua đen: hàng dưới
            if king_col > 0:  # Kiểm tra biên trái
                if isinstance(board.board[king_row + 1][king_col - 1], Pawn) and \
                   board.board[king_row + 1][king_col - 1].color == color:
                    left_pawn_check = True
            if king_col < 7:  # Kiểm tra biên phải
                if isinstance(board.board[king_row + 1][king_col + 1], Pawn) and \
                   board.board[king_row + 1][king_col + 1].color == color:
                    right_pawn_check = True
        if not left_pawn_check:
            score -= 0.1
        if not right_pawn_check:
            score -= 0.1

        # 4. Đếm quân cùng màu bảo vệ các ô xung quanh vua
        king = board.board[king_row][king_col]
        king_valid_moves = king.get_valid_moves(board)  # Các ô vua có thể đến
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.color == color and piece != king:  # Không tính chính vua
                    valid_moves = piece.get_valid_moves(board)
                    for move in valid_moves:
                        if move in king_valid_moves:
                            score += 0.05

        return score
    

    # 4. Pawn structure (Cấu trúc tốt)
    def evaluate_pawn_structure_score(self, board: Board, color):
        score = 0
        opponent_color = "white" if color == "black" else "black"

        # Đếm số tốt trên mỗi cột
        pawn_columns = [[] for _ in range(8)]  # Danh sách các hàng có tốt theo cột
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, Pawn) and piece.color == color:
                    pawn_columns[col].append(row)

        # 1. Tốt thừa (từ tốt thứ 2 trở lên trong cùng cột): -0.1 điểm
        for col in range(8):
            if len(pawn_columns[col]) > 1:
                score -= 0.1 * (len(pawn_columns[col]) - 1)  # Phạt cho mỗi tốt thừa

        # Duyệt từng tốt để tính các yếu tố khác
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, Pawn) and piece.color == color:
                    # 2. Tốt thông: +0.15, gần phong cấp +0.25
                    is_passed = True
                    for check_col in range(max(0, col - 1), min(8, col + 2)):  # Kiểm tra cột bên cạnh
                        for check_row in range(8):
                            if color == "white" and check_row < row:  # Bỏ qua hàng phía sau tốt trắng
                                continue
                            if color == "black" and check_row > row:  # Bỏ qua hàng phía sau tốt đen
                                continue
                            if isinstance(board.board[check_row][check_col], Pawn) and board.board[check_row][check_col].color == opponent_color:
                                is_passed = False
                                break
                        if not is_passed:
                            break
                    if is_passed:
                        if (color == "white" and row < 3) or (color == "black" and row > 4):
                            score += 0.25  # Gần phong cấp
                        else:
                            score += 0.15  # Tốt thông bình thường

                    # 3. Tốt lạc hậu: -0.2 điểm
                    is_backward = False
                    if color == "white" and row < 7:  # Tốt trắng: kiểm tra hàng trên
                        for check_col in range(max(0, col - 1), min(8, col + 2)):
                            if isinstance(board.board[row + 1][check_col], Pawn) and board.board[row + 1][check_col].color == color:
                                is_backward = True
                                break
                    elif color == "black" and row > 0:  # Tốt đen: kiểm tra hàng dưới
                        for check_col in range(max(0, col - 1), min(8, col + 2)):
                            if isinstance(board.board[row - 1][check_col], Pawn) and board.board[row - 1][check_col].color == color:
                                is_backward = True
                                break
                    if is_backward and not is_passed:  # Tốt lạc hậu phải không thông
                        score -= 0.2

                    # 4. Tốt nối liền: +0.1 điểm
                    is_connected = False
                    for adj_col in (col - 1, col + 1):
                        if 0 <= adj_col < 8:
                            for adj_row in range(max(0, row - 1), min(8, row + 2)):
                                if isinstance(board.board[adj_row][adj_col], Pawn) and board.board[adj_row][adj_col].color == color:
                                    is_connected = True
                                    break
                            if is_connected:
                                break
                    if is_connected:
                        score += 0.1

        return score
    