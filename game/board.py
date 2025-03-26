from game.pieces import King, Knight, Queen, Pawn, Rook, Bishop
from game.move_generator import MoveGenerator
from copy import deepcopy

class Board:
    def __init__(self):
        self.piece = {
            'K': King,
            'Q': Queen,
            'N': Knight,
            'P': Pawn,
            'R': Rook,
            'B': Bishop,
        }
        self.board = self.setup_board()
        self.move_log = [] # Lịch sử nước đi có định dạng như sau: ((x1, y1), (x2, y2), piece)
        self.turn = "white"

    def __str__(self):
        # Chuyển trạng thái bàn cờ thành một chuỗi dễ đọc
        board_rep = ""
        for row in self.board:
            board_rep += " ".join([str(cell) if cell else "." for cell in row]) + "\n"
        return board_rep
    
    def setup_board(self):
        """Khởi tạo bàn cờ với các quân cờ đúng vị trí"""
        board = [[None] * 8 for _ in range(8)]  # Tạo ma trận 8x8 rỗng

        # Đặt quân trắng
        board[7] = [Rook((7, 0), "white"), Knight((7, 1), "white"), Bishop((7, 2), "white"), 
                    Queen((7, 3), "white"), King((7, 4), "white"), Bishop((7, 5), "white"), 
                    Knight((7, 6), "white"), Rook((7, 7), "white")]
        board[6] = [Pawn((6, i), "white") for i in range(8)]

        # Đặt quân đen
        board[0] = [Rook((0, 0), "black"), Knight((0, 1), "black"), Bishop((0, 2), "black"), 
                    Queen((0, 3), "black"), King((0, 4), "black"), Bishop((0, 5), "black"), 
                    Knight((0, 6), "black"), Rook((0, 7), "black")]
        board[1] = [Pawn((1, i), "black") for i in range(8)]

        return board
    
    def get_legal_moves(self):
        legal_moves = []
        move_generator = MoveGenerator(self)
        legal_moves = move_generator.get_legal_moves()
        return legal_moves

    # Hàm đổi lượt
    def switch_turns(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    # Tạo trạng thái dựa trên move
    def generate_state_from_a_move(self, move):
        temp_board = deepcopy(self)  # Tạo bản sao của bàn cờ
        pre_x, pre_y = move[0]
        new_x, new_y = move[1]
        
        # Lấy quân cờ từ bàn cờ đã sao chép
        piece = temp_board.board[pre_x][pre_y]
        
        # Lưu thông tin quân cờ trước khi di chuyển để thêm vào move_log
        piece_info = (pre_x, pre_y, type(piece).__name__, piece.color)
        
        # Di chuyển quân cờ trên bản sao
        piece.move((new_x, new_y), temp_board)
        
        # Thêm vào move_log của bản sao
        temp_board.move_log.append((move[0], move[1], piece))
        
        # Đổi lượt chơi trên bản sao
        temp_board.switch_turns()
        
        return temp_board
    
    # Tạo tất cả trạng thái có thể xảy ra
    def generate_all_states(self):
        legal_states = []
        legal_moves = self.get_legal_moves()
        for move in legal_moves:
            temp_board = self.generate_state_from_a_move(move)
            legal_states.append(temp_board)  # Thêm bản sao vào danh sách
        return legal_states

    def is_in_check(self, color):
        # Tìm vị trí của vua
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
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
                piece = self.board[row][col]
                if piece and piece.color != color:
                    valid_moves = piece.get_valid_moves(self)
                    if king_position in valid_moves:
                        return True
        return False


