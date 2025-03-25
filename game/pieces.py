# game/pieces.py
from abc import ABC, abstractmethod

class Pieces:
    def __init__(self, position: list[int], color: str):
        self.position = tuple(position)
        self.color = color

    @abstractmethod
    def get_valid_moves(self, board, last_move=None):
        pass

    @abstractmethod
    def __str__(self):
        pass 

    def move(self, new_position, board):
        from game.board import Board  # Import tại đây
        pre_x, pre_y = self.position
        new_x, new_y = new_position
        board.board[new_x][new_y] = self
        board.board[pre_x][pre_y] = None
        self.position = tuple(new_position)

class King(Pieces):
    def get_valid_moves(self, board, last_move=None):
        from game.board import Board  # Import tại đây
        valid_moves = []
        x, y = self.position
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if (board.board[nx][ny] is None) or (board.board[nx][ny] is not None and self.color != board.board[nx][ny].color):
                    valid_moves.append((nx, ny))
        
        available_castling = self.check_castling(board)
        if available_castling == "a":
            valid_moves.append((x, y - 2))
        elif available_castling == "h":
            valid_moves.append((x, y + 2))
        elif available_castling == "both":
            valid_moves.append((x, y - 2))
            valid_moves.append((x, y + 2))
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♚"
        return "♔"

    def check_castling(self, board):
        from game.board import Board  # Import tại đây
        if self.color == "white":
            king_start = (7, 4)
            row = 7
        else:
            king_start = (0, 4)
            row = 0

        if tuple(self.position) != king_start or self.is_square_attacked(board, king_start):
            return "no_castling"

        for log in board.move_log:
            (pre_x, pre_y), (new_x, new_y), piece = log
            if isinstance(piece, King) and self.color == piece.color:
                return "no_castling"
        
        rook_a_check = True
        rook_h_check = True
        for log in board.move_log:
            (pre_x, pre_y), (new_x, new_y), piece = log
            if isinstance(piece, Rook) and self.color == piece.color:
                if pre_y == 0:
                    rook_a_check = False
                elif pre_y == 7:
                    rook_h_check = False
        if not rook_a_check and not rook_h_check:
            return "no_castling"
        
        if rook_a_check:
            for col in range(1, 4):
                if board.board[row][col] is not None or self.is_square_attacked(board, (row, col)):
                    rook_a_check = False

        if rook_h_check:
            for col in range(5, 7):
                if board.board[row][col] is not None or self.is_square_attacked(board, (row, col)):
                    rook_h_check = False

        if rook_a_check and rook_h_check:
            return "both"
        elif rook_a_check:
            return "a"
        elif rook_h_check:
            return "h"
        else:
            return "no_castling"

    def is_square_attacked(self, board, square):
            for row in range(8):
                for col in range(8):
                    piece = board.board[row][col]
                    # Bỏ qua quân King để tránh đệ quy vô hạn
                    if piece and piece.color != self.color and not isinstance(piece, King):
                        valid_moves = piece.get_valid_moves(board)
                        if square in valid_moves:
                            return True
            return False

class Queen(Pieces):
    def get_valid_moves(self, board, last_move=None):
        from game.board import Board  # Import tại đây
        valid_moves = []
        x, y = self.position
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board.board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                else:  # Gặp quân cờ (cùng màu hoặc khác màu)
                    if self.color != board.board[nx][ny].color:  # Quân địch
                        valid_moves.append((nx, ny))
                    break  # Dừng lại khi gặp bất kỳ quân cờ nào
                nx += dx
                ny += dy
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♛"
        return "♕"

class Rook(Pieces):
    def get_valid_moves(self, board, last_move=None):
        from game.board import Board  # Import tại đây
        valid_moves = []
        x, y = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board.board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                else:  # Gặp quân cờ (cùng màu hoặc khác màu)
                    if self.color != board.board[nx][ny].color:  # Quân địch
                        valid_moves.append((nx, ny))
                    break  # Dừng lại khi gặp bất kỳ quân cờ nào
                nx += dx
                ny += dy
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♜"
        return "♖"

class Bishop(Pieces):
    def get_valid_moves(self, board, last_move=None):
        from game.board import Board  # Import tại đây
        valid_moves = []
        x, y = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board.board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                else:  # Gặp quân cờ (cùng màu hoặc khác màu)
                    if self.color != board.board[nx][ny].color:  # Quân địch
                        valid_moves.append((nx, ny))
                    break  # Dừng lại khi gặp bất kỳ quân cờ nào
                nx += dx
                ny += dy
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♝"
        return "♗"

class Knight(Pieces):
    def get_valid_moves(self, board, last_move=None):
        from game.board import Board  # Import tại đây
        valid_moves = []
        x, y = self.position
        jumps = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
        for dx, dy in jumps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if (board.board[nx][ny] is None) or (board.board[nx][ny] is not None and self.color != board.board[nx][ny].color):
                    valid_moves.append((nx, ny))
        return valid_moves

    def __str__(self):
        if self.color == "white":
            return "♞"
        return "♘"

class Pawn(Pieces):
    def get_valid_moves(self, board, last_move=None):
        from game.board import Board  # Import tại đây
        valid_moves = []
        x, y = self.position
        if self.color == "white":
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        if 0 <= x + direction < 8 and board.board[x + direction][y] is None:
            valid_moves.append((x + direction, y))
            if x == start_row and board.board[x + 2 * direction][y] is None:
                valid_moves.append((x + 2 * direction, y))

        for dy in [-1, 1]:
            new_x, new_y = x + direction, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.board[new_x][new_y]
                if target is not None and target.color != self.color:
                    valid_moves.append((new_x, new_y))

        if last_move:
            (prev_x, prev_y), (new_x, new_y), moved_piece = last_move
            if (isinstance(moved_piece, Pawn) and 
                abs(prev_x - new_x) == 2 and
                new_x == x and abs(new_y - y) == 1):
                valid_moves.append((x + direction, new_y))

        return valid_moves


    def __str__(self):
        return "♟" if self.color == "white" else "♙"
    
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