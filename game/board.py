from pieces import King, Knight, Queen, Pawn, Rook, Bishop

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
        self.board = []
        for i in range(8):
            self.board.append([None] * 8) # 8 columns each row

    def __str__(self):
        # Chuyển trạng thái bàn cờ thành một chuỗi dễ đọc
        board_rep = ""
        for row in self.board:
            board_rep += " ".join([str(cell) if cell else "." for cell in row]) + "\n"
        return board_rep
    
    def convert_valid_position(self, pos):
        x = 8 - int(pos[1])
        y = pos[0]
        if y == 'a':
            y = 0
        elif y == 'b':
            y = 1
        elif y == 'c':
            y = 2
        elif y == 'd':
            y = 3
        elif y == 'e':
            y = 4
        elif y == 'f':
            y = 5
        elif y == 'g':
            y = 6
        elif y == 'h':
            y = 7
        else:
            return "This is invalid position"
        return x, y
    
    def place_piece(self, piece_name, pos):
        x, y = self.convert_valid_position(pos)
        # Kiểm tra x, y có nằm trong phạm vi bàn cờ
        if not (0 <= x < 8 and 0 <= y < 8):
            return "Position out of bounds"
        
        piece_upper = piece_name.upper()
        
        if piece_upper in self.piece:
            self.board[x][y] = self.piece[piece_upper]([x, y])
        else:
            return "Invalid Piece"

    def remove_piece(self, pos):
        x, y = self.convert_valid_position(pos)
        self.board[x][y] = None
        
    def count_NumberOfPieces(self):
        cnt = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    cnt += 1
        return cnt
    
    def get_board_valid_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    piece = self.board[i][j]
                    moves = piece.get_valid_moves(self.board)
                    for move in moves:
                        valid_moves.append((i, j, move[0], move[1]))  # (from_x, from_y, to_x, to_y)

        return valid_moves
    
    def update_board(self, move):
        x_old, y_old, x_new, y_new = move
        
        # Lấy quân cờ đang di chuyển
        moving_piece = self.board[x_old][y_old]
        
        if moving_piece is None:
            raise ValueError("Invalid move: No piece at the starting position")
        
        # Di chuyển quân cờ
        self.board[x_new][y_new] = moving_piece
        self.board[x_old][y_old] = None
        
        # Cập nhật vị trí của quân cờ
        self.board[x_new][y_new].position = [x_new, y_new]


