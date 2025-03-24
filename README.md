# Chess Bot Game

## Overview
Chess Bot Game is a Python-based chess game that allows players to compete against AI bots of varying difficulty levels. The project is structured into several modules, each responsible for different aspects of the game, including bot algorithms, game logic, user interface, and testing.

## Project Structure
```
chess_bot_game/
├── bots/                     # Contains AI bot algorithms
│   ├── __init__.py
│   ├── base_bot.py           # Base class for all bots
│   ├── easy_bot.py           # Easy difficulty bot
│   ├── medium_bot.py         # Medium difficulty bot
│   ├── hard_bot.py           # Hard difficulty bot
├── game/                     # Contains the main game logic
│   ├── __init__.py
│   ├── board.py              # Manages the game board and moves
│   ├── pieces.py             # Manages chess pieces
│   ├── move_generator.py      # Generates valid moves
│   ├── evaluator.py          # Evaluates board positions
│   ├── alpha_beta.py         # Implements Alpha-Beta Pruning
├── ui/                       # User interface components
│   ├── __init__.py
│   ├── streamlit_ui.py       # Streamlit user interface
│   ├── pygame_ui.py          # Pygame user interface
├── assets/                   # Contains resources like images and sounds
│   ├── chess_pieces/         # Images of chess pieces
│   ├── sounds/               # Sound files for the game
├── tests/                    # Contains test files
│   ├── test_board.py         # Tests for board functionality
│   ├── test_alpha_beta.py    # Tests for Alpha-Beta algorithm
│   ├── test_bots.py          # Tests for AI bots
├── main.py                   # Entry point to run the game
├── requirements.txt          # List of required libraries
└── README.md                 # Project documentation
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd chess_bot_game
pip install -r requirements.txt
```

## Usage
To run the game, execute the following command:

```bash
python main.py
```

You can choose to play against different AI bots by selecting the desired difficulty level in the user interface.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.