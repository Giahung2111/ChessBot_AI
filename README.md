# Chess Bot Game

A Python-based chess game where you can play against AI bots with different difficulty levels. The game features both Pygame user interfaces.

## Features

- Play chess against AI bots with 3 difficulty levels
- Two user interface options: Pygame (graphical)
- Smart AI using Alpha-Beta pruning algorithm
- Beautiful chess piece graphics
- Sound effects for moves and captures
- Move validation and game state tracking
- Support for both light and dark themes

## Requirements

- Python 3.8 or higher
- Pygame
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Giahung2111/ChessBot_AI.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

### Using Pygame Interface
1. Run the game:
```bash
python main.py
```

2. Choose your color (white or black)
3. Select bot difficulty level (1-3)
4. Play the game using mouse clicks

## Game Controls

- Click on a piece to select it
- Click on a valid square to move the piece
- Press ESC to exit the game
- Press R to reset the game

## Bot Difficulty Levels

1. **Easy (Level 1)**
   - Uses simple evaluation
   - Makes basic moves
   - Good for beginners

2. **Medium (Level 2)**
   - Uses Alpha-Beta pruning
   - Looks ahead 2 moves
   - Balanced challenge

3. **Hard (Level 3)**
   - Advanced Alpha-Beta pruning
   - Looks ahead 3 moves
   - Challenging for experienced players

## Project Structure

```
chess_bot_game/
├── bots/                     # AI bot code
│   ├── bot.py               # Main bot logic
│   └── alpha_beta.py        # Alpha-Beta algorithm
├── game/                    # Game logic
│   ├── board.py            # Board management
│   ├── pieces.py           # Chess pieces
│   └── move_generator.py   # Move validation
│   └── alpha_beta.py        # Minimax algorithm
├── ui/                      # User interfaces
│   ├── pygame_ui.py        # Pygame interface
├── assets/                  # Game resources
│   ├── chess_pieces/       # Piece images
│   └── sounds/             # Sound effects
└── main.py                 # Game entry point
```

## How the AI Works

The bot uses the Alpha-Beta pruning algorithm to:
1. Look ahead several moves
2. Evaluate board positions
3. Choose the best move based on:
   - Piece values
   - Position control
   - King safety
   - Material advantage

## Contributing

Feel free to:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

If you experience issues:
1. Make sure all requirements are installed
2. Check if your Python version is compatible
3. Verify that all asset files are present
4. Try running with a lower bot difficulty level

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits

- Chess piece images: [Source]
- Sound effects: [Source]
- Alpha-Beta algorithm implementation based on chess programming principles

## Support

If you need help or have questions:
1. Check the documentation
2. Open an issue
3. Contact the maintainers

Enjoy playing Chess Bot Game!