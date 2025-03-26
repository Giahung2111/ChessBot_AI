import pygame
from pygame.locals import *
from game.board import Board
from bots.bot import Bot

# Khởi tạo Pygame
pygame.init()

# Đặt kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Bot Game")

# Định nghĩa màu và kích thước ô
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
SQUARE_SIZE = SCREEN_WIDTH // 8

# Tải hình ảnh quân cờ
PIECE_IMAGES = {
    'white_Pawn': pygame.image.load('assets/chess_pieces/w_pawn.png'),
    'white_Rook': pygame.image.load('assets/chess_pieces/w_rook.png'),
    'white_Knight': pygame.image.load('assets/chess_pieces/w_knight.png'),
    'white_Bishop': pygame.image.load('assets/chess_pieces/w_bishop.png'),
    'white_Queen': pygame.image.load('assets/chess_pieces/w_queen.png'),
    'white_King': pygame.image.load('assets/chess_pieces/w_king.png'),
    'black_Pawn': pygame.image.load('assets/chess_pieces/b_pawn.png'),
    'black_Rook': pygame.image.load('assets/chess_pieces/b_rook.png'),
    'black_Knight': pygame.image.load('assets/chess_pieces/b_knight.png'),
    'black_Bishop': pygame.image.load('assets/chess_pieces/b_bishop.png'),
    'black_Queen': pygame.image.load('assets/chess_pieces/b_queen.png'),
    'black_King': pygame.image.load('assets/chess_pieces/b_king.png'),
}
for key in PIECE_IMAGES:
    PIECE_IMAGES[key] = pygame.transform.scale(PIECE_IMAGES[key], (SQUARE_SIZE - 20, SQUARE_SIZE - 20))

# Hàm vẽ bàn cờ
def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Hàm vẽ quân cờ
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                piece_key = f"{piece.color}_{type(piece).__name__}"
                screen.blit(PIECE_IMAGES[piece_key], (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10))

# Hàm xử lý sự kiện chuột
def handle_mouse_click(pos, board, selected_piece, selected_pos):
    col = pos[0] // SQUARE_SIZE
    row = pos[1] // SQUARE_SIZE
    if selected_piece is None:
        piece = board.board[row][col]
        if piece and piece.color == board.turn:
            print(f"Đã chọn quân cờ: {piece} tại ({row}, {col})")  # Debug
            return piece, (row, col)
    else:
        move = (selected_pos, (row, col)) # Nước đi của player
        legal_moves = board.get_legal_moves() # Các nước đi hợp lệ
        if move in legal_moves: # Kiểm tra xem nước đi của người dùng có hợp lệ hay không ?
            print(f"Di chuyển từ {selected_pos} đến ({row}, {col})")  # Debug
            selected_piece.move((row, col), board)
            board.move_log.append((selected_pos, (row, col), selected_piece)) # Thêm vào lịch sử
            board.switch_turns() # Đổi lượt
            return None, None
        else:
            print(f"Nước đi không hợp lệ: {move}")  # Debug
            return None, None
    return selected_piece, selected_pos

# Hàm kiểm tra kết thúc game
def check_game_over(board):
    legal_moves = board.get_legal_moves()
    if len(legal_moves) == 0:
        if board.is_in_check(board.turn):
            winner = "White" if board.turn == "black" else "Black" # Trắng sẽ thắng nếu đen hết nước đi hợp lệ
            return f"Checkmate! {winner} win!"
        else:
            return "Draw! Stalemate!"
    return None

# Hàm vẽ thông tin game
font = pygame.font.Font(None, 36)
def draw_game_info(board):
    turn_text = font.render(f"This is {board.turn}'s turn", True, (0, 0, 0))
    screen.blit(turn_text, (10, 10))
    if board.is_in_check(board.turn):
        check_text = font.render("The King is in check", True, (255, 0, 0))
        screen.blit(check_text, (10, 50))
    game_over = check_game_over(board)
    if game_over:
        over_text = font.render(game_over, True, (0, 0, 0))
        screen.blit(over_text, (10, 90))
        return True  # Thêm giá trị trả về để biết game kết thúc
    return False

def run_pygame_ui(level=3, bot_color="black"):
    # Khởi tạo board và bot
    board = Board()
    bot = Bot(level=level, bot_color=bot_color)

    # Biến theo dõi quân cờ được chọn
    selected_piece = None
    selected_pos = None
    
    # Biến kiểm tra game đã kết thúc chưa
    game_over = False

    # Vòng lặp chính
    running = True
    clock = pygame.time.Clock()  # Thêm clock để kiểm soát FPS
    while running:
        ## Lượt đi của người chơi
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and not game_over:
                selected_piece, selected_pos = handle_mouse_click(event.pos, board, selected_piece, selected_pos)
                # Vẽ lại ngay sau khi người chơi di chuyển
                if selected_piece is None and selected_pos is None:
                    draw_board()
                    draw_pieces(board)
                    game_over = draw_game_info(board)
                    pygame.display.flip()

        ## Lượt đi của bot
        # Chỉ cho bot đi khi đến lượt, người chơi đã hoàn thành nước đi và game chưa kết thúc
        if board.turn == bot.color and selected_piece is None and not game_over:
            print(f"Lượt của bot ({bot_color})")  # Debug
            print("Trạng thái bàn cờ trước khi bot di chuyển:")
            print(board)
            bot.make_move(board)
            board.switch_turns()
            # Vẽ lại sau khi bot di chuyển
            draw_board()
            draw_pieces(board)
            game_over = draw_game_info(board)
            pygame.display.flip()

        # Vẽ lại giao diện
        draw_board()
        draw_pieces(board)
        game_over = draw_game_info(board)
        pygame.display.flip()
        clock.tick(60)  # Giới hạn 60 FPS

    pygame.quit()