from game.alpha_beta import AlphaBeta
import time

class Bot:
    def __init__(self, level, bot_color):
        # Chiều cao duyệt cây (Tương ứng với độ khó của bot)
        self.level = level
        self.color = bot_color
        # Giới hạn thời gian tối đa cho mỗi nước đi (giây)
        self.time_limit = 5.0

    def make_move(self, board):
        try:
            ab = AlphaBeta(self.level, self.color)
            
            # Bắt đầu đếm thời gian
            start_time = time.time()
            
            # Tìm nước đi tốt nhất với giới hạn thời gian
            best_move = None
            score = 0
            try:
                best_move, score = ab.find_best_move(board)
            except TimeoutError:
                print("Bot hết thời gian tính toán, sử dụng nước đi tốt nhất tìm được")
            
            # Kiểm tra thời gian đã dùng
            elapsed_time = time.time() - start_time
            if elapsed_time > self.time_limit:
                print(f"Bot đã dùng {elapsed_time:.2f} giây để tính toán")
            
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
            
            # Đảm bảo quân cờ tồn tại tại vị trí xuất phát
            piece = board.board[pre_x][pre_y]
            if piece is None:
                raise ValueError(f"Không có quân cờ tại vị trí {pre_x}, {pre_y}")
            
            # Đảm bảo quân cờ thuộc về bot
            if piece.color != self.color:
                raise ValueError(f"Quân cờ tại {pre_x}, {pre_y} không phải màu của bot")
            
            # Thực hiện nước đi của bot
            print(f"Bot di chuyển {piece} từ {best_move[0]} đến {best_move[1]}")
            piece.move((new_x, new_y), board)
            
            # Thêm nước đi vào move_log
            board.move_log.append((best_move[0], best_move[1], piece))
            
            # Kiểm tra xem bot có chiếu hết người chơi không
            board.switch_turns()  # Đổi lượt tạm thời để kiểm tra
            if len(board.get_legal_moves()) == 0 and board.is_in_check(board.turn):
                print(f"Bot ({self.color}) đã chiếu hết người chơi!")
            board.switch_turns()  # Đổi lại lượt vì sẽ đổi lượt trong pygame_ui
            
        except Exception as e:
            print(f"Lỗi khi bot thực hiện nước đi: {e}")
            # Đảm bảo trò chơi tiếp tục ngay cả khi có lỗi
            print("Bot bỏ lượt do lỗi xảy ra.")
