from game.alpha_beta import AlphaBeta

class Bot:
    def __init__(self, level, bot_color):
        # Chiều cao duyệt cây (Tương ứng với độ khó của bot)
        self.level = level
        self.color = bot_color

    def make_move(self, board):
        ab = AlphaBeta(self.level, self.color)
        best_move, score = ab.find_best_move(board)
        print(f"Nước đi tốt nhất: {best_move}, Điểm: {score}")
        if best_move is None:
            # Không có nước đi hợp lệ, kiểm tra xem bot thua hay hòa
            legal_moves = board.get_legal_moves()
            if len(legal_moves) == 0:
                if board.is_in_check(self.color):
                    print(f"Bot ({self.color}) thua vì bị chiếu hết!")
                else:
                    print("Hòa do bế tắc!")
            return  # Thoát hàm mà không thực hiện nước đi

        if not isinstance(best_move, tuple) or len(best_move) != 2:
            raise ValueError(f"Invalid move format: {best_move}")
        pre_x, pre_y = best_move[0]
        new_x, new_y = best_move[1]
        piece = board.board[pre_x][pre_y]
        piece.move((new_x, new_y), board)  # Di chuyển quân cờ 
