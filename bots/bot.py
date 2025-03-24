from game.alpha_beta import AlphaBeta

class Bot:
    def __init__(self, level):
        # Chiều cao duyệt cây (Tương ứng với độ khó của bot)
        self.level = level

    def make_move(self, board):
        ab = AlphaBeta(self.level)
        best_move, score = ab.find_best_move(board)
        print(f"Nước đi tốt nhất: {best_move}, Điểm: {score}")
        # Bổ sung thêm di chuyển sau này (Nhắc nhở)
