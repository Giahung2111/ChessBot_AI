import math
from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn

class AlphaBeta:
    def evaluate_board(self, board: Board):
        """
        Hàm đánh giá bàn cờ nâng cao.
        Đánh giá dựa trên:
        - Giá trị vật chất của quân cờ.
        - Vị trí của quân cờ (dùng bảng vị trí).
        - Sự di động của quân cờ.
        - An toàn của vua.
        - Cấu trúc tốt (đơn giản).
        """
        # Kiểm tra trạng thái kết thúc
        if board.is_checkmate():
            return -math.inf if board.turn == "white" else math.inf
        if board.is_stalemate():
            return 0  # Hòa

        score = 0

        # 1. Giá trị vật chất
        score += self.material_score(board)

        # 2. Điểm vị trí
        score += self.position_score(board)

        # 3. Điểm di động
        score += self.mobility_score(board)

        # 4. An toàn của vua
        score += self.king_safety_score(board)

        # 5. Cấu trúc tốt
        score += self.pawn_structure_score(board)

        return score

    def material_score(self, board: Board):
        """Tính điểm dựa trên giá trị vật chất của quân cờ."""
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}  # Vua không có giá trị vật chất
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece:
                    value = piece_values.get(piece.__class__.__name__[0], 0)
                    if piece.color == board.turn:
                        score += value
                    else:
                        score -= value
        return score

    def position_score(self, board: Board):
        """Tính điểm dựa trên vị trí của quân tốt."""
        pawn_table_white = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
            [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
            [0.0, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0],
            [0.05, -0.05, -0.1, 0.0, 0.0, -0.1, -0.05, 0.05],
            [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        pawn_table_black = pawn_table_white[::-1]  # Đảo ngược cho quân đen

        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, Pawn):
                    if piece.color == "white":
                        score += pawn_table_white[row][col]
                    else:
                        score += pawn_table_black[row][col]
        return score

    def mobility_score(self, board: Board):
        """Tính điểm dựa trên số nước đi hợp lệ."""
        bot_moves = len(board.get_legal_moves()) if board.turn == "white" else -len(board.get_legal_moves())
        board.switch_turns()
        opponent_moves = len(board.get_legal_moves()) if board.turn != "white" else -len(board.get_legal_moves())
        board.switch_turns()  # Khôi phục lượt
        return 0.1 * (bot_moves - opponent_moves)

    def king_safety_score(self, board: Board):
        """Tính điểm dựa trên số quân bảo vệ vua."""
        score = 0
        for color in ["white", "black"]:
            king_pos = self.find_king(board, color)
            if king_pos:
                defenders = self.count_defenders(board, king_pos, color)
                if color == board.turn:
                    score += 0.5 * defenders
                else:
                    score -= 0.5 * defenders
        return score

    def find_king(self, board: Board, color):
        """Tìm vị trí của vua."""
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def count_defenders(self, board: Board, pos, color):
        """Đếm số quân cùng màu bảo vệ ô pos."""
        defenders = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.color == color:
                    if pos in piece.get_valid_moves(board):
                        defenders += 1
        return defenders

    def pawn_structure_score(self, board: Board):
        """Tính điểm dựa trên cấu trúc tốt."""
        score = 0
        for color in ["white", "black"]:
            pawns = self.get_pawns(board, color)
            isolated, doubled = self.analyze_pawn_structure(pawns)
            penalty = -0.5 * isolated - 0.5 * doubled
            if color == board.turn:
                score += penalty
            else:
                score -= penalty
        return score

    def get_pawns(self, board: Board, color):
        """Lấy danh sách vị trí các tốt."""
        pawns = []
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if isinstance(piece, Pawn) and piece.color == color:
                    pawns.append((row, col))
        return pawns

    def analyze_pawn_structure(self, pawns):
        """Phân tích cấu trúc tốt: đếm tốt cô lập và tốt đôi."""
        files = [[] for _ in range(8)]
        for row, col in pawns:
            files[col].append(row)
        
        isolated = 0
        doubled = 0
        for col in range(8):
            if files[col]:
                if len(files[col]) > 1:
                    doubled += len(files[col]) - 1
                if (col == 0 and not files[1]) or (col == 7 and not files[6]) or \
                   (0 < col < 7 and not files[col-1] and not files[col+1]):
                    isolated += len(files[col])
        return isolated, doubled