# main.py
import asyncio
import platform
from game.board import Board
from ui.pygame_ui import run_pygame_ui, watch_bots

def main():
    print("Starting Chess Bot Game with Pygame UI...")
    print("Chọn chế độ chơi:")
    print("1. Người đấu với Bot")
    print("2. Xem 2 Bot đấu nhau")
    
    while True:
        choice = input("Nhập lựa chọn (1 hoặc 2): ")
        if choice == "1":
            run_pygame_ui(level=2, bot_color="black")  # Người đấu với bot
            break
        elif choice == "2":
            watch_bots(bot_level=1, bot_color="black", random_bot_level=0)  # 2 bot đấu nhau
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại!")

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())