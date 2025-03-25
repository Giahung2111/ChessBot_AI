# main.py
from game.board import Board
from ui.pygame_ui import run_pygame_ui

def main():
    print("Starting Chess Bot Game with Pygame UI...")
    run_pygame_ui(level = 2, bot_color = "black")

if __name__ == "__main__":
    main()