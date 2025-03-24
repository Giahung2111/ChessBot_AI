from abc import ABC, abstractmethod

class Pieces:
    def __init__(self, position: list[int], color: str):
        self.position = position
        self.color = color

    @abstractmethod
    def get_valid_moves(self, board):
        pass

    @abstractmethod
    def __str__(self):
        pass 

    def move(self, new_position):
        self.position = new_position

class King(Pieces):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:  # Trong bàn cờ
                if (board[nx][ny] is None) or ( board[nx][ny] is not None and self.color != board[nx][ny].color):  # Ô chứa quân khác
                    valid_moves.append((nx, ny))
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♚"
        return "♔"

class Queen(Pieces):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                elif board[nx][ny] is not None and self.color != board[nx][ny].color:
                    valid_moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♛"
        return "♕"

class Rook(Pieces):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                elif board[nx][ny] is not None and self.color != board[nx][ny].color:
                    valid_moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♜"
        return "♖"

class Bishop(Pieces):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                elif board[nx][ny] is not None and self.color != board[nx][ny].color:
                    valid_moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♝"
        return "♗"

class Knight(Pieces):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position
        jumps = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
        for dx, dy in jumps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if (board[nx][ny] is None) or (board[nx][ny] is not None and self.color != board[nx][ny].color):
                    valid_moves.append((nx, ny))
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♞"
        return "♘"

class Pawn(Pieces):
    def get_valid_moves(self, board, last_move=None):
        valid_moves = []
        x, y = self.position

        # Xác định hướng và hàng đặc biệt dựa trên màu
        if self.color == "white":
            direction = -1  # Trắng đi lên (giảm số hàng)
            start_row = 6   # Hàng bắt đầu của trắng
            # promotion_row = 0  # Hàng phong cấp của trắng
        else:  # self.color == "black"
            direction = 1  # Đen đi xuống (tăng số hàng)
            start_row = 1  # Hàng bắt đầu của đen
            # promotion_row = 7  # Hàng phong cấp của đen

        # 1. Tiến một ô nếu không bị chặn
        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            valid_moves.append((x + direction, y))
            # 2. Tiến hai ô nếu ở vị trí ban đầu và không bị chặn
            if x == start_row and board[x + 2 * direction][y] is None:
                valid_moves.append((x + 2 * direction, y))

        # 3. Ăn chéo
        for dy in [-1, 1]:  # Chéo trái và phải
            new_x, new_y = x + direction, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board[new_x][new_y]
                if target is not None and target.color != self.color:
                    valid_moves.append((new_x, new_y))

        # 4. Bắt chốt qua đường (en passant)
        if last_move:
            (prev_x, prev_y), (new_x, new_y), moved_piece = last_move
            if (isinstance(moved_piece, Pawn) and 
                abs(prev_x - new_x) == 2 and  # Đối phương vừa đi 2 ô
                new_x == x and abs(new_y - y) == 1):  # Ngang hàng và cạnh nhau
                valid_moves.append((x + direction, new_y))

        return valid_moves

    # def move(self, new_position, board):
    #     """Di chuyển quân cờ và xử lý phong cấp."""
    #     x, y = new_position

    #     # Nếu đạt đến hàng phong cấp, biến thành quân Hậu (mặc định)
    #     if x == (0 if self.color == "white" else 7):
    #         print(f"Pawn tại {self.position} đã phong cấp! Chọn quân mới (Q/R/B/N):")
    #         choice = input().upper()
    #         if choice == "R":
    #             board[x][y] = Rook([x, y])
    #         elif choice == "B":
    #             board[x][y] = Bishop([x, y])
    #         elif choice == "N":
    #             board[x][y] = Knight([x, y])
    #         else:
    #             board[x][y] = Queen([x, y])  # Mặc định phong cấp thành Hậu
    #     else:
    #         board[x][y] = self  # Di chuyển chốt bình thường

    #     self.position = [x, y]

    def __str__(self):
        return "♟" if self.color == "white" else "♙"