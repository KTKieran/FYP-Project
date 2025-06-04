# Sokoban Game Project

# Overview
This Sokoban project is a modern implementation of the classic puzzle game where a player must push boxes to specific locations  a grid layout. The game is developed in Python using the Pygame library, emphasizing clear structure and modular design to facilitate easy updates and modifications. The project expands on solution pathing within a puzzle game, finding a goal state and displaying the most optimal path.

# Features
Graphical User Interface: Utilizes Pygame for rendering the game state, including a grid-based level design, interactive buttons, and game elements such as walls (black), boxes (brown), targets (silver), and the player (blue).
6 playable Levels: Includes 6 predefined levels with varying complexity.
A* Search Algorithm: Implements an AI solver using the A* search algorithm to automatically solve the levels. The solver considers both the actual steps taken and a heuristic to minimize the moves required to solve the puzzles.
Interactive Controls: Players can use keyboard arrows to move the player character and push boxes. The game also includes clickable buttons for solving the game automatically and resetting to the original level state.
Animation and Visual Feedback: Provides visual feedback for actions, including movement animations and state changes when solving puzzles.

# Library implements
Python 3.x
Pygame

- To install Pygame, run:

```
    pip install pygame
```

# Setup and Running the Game
- Clone the repository:

```
    git clone [repository URL]
    cd [local repository]
```
 
- Run the game:

```
    python main.py
```

# Game Controls
Arrow Keys: Move the player up, down, left, or right.
Solve Button: Click to trigger the AI interaction and to automatically solve the current level.
Reset Button: Click to reset the level to its initial state.

# Modules
main.py: The main game loop and event handling.
settings.py: Contains game settings such as screen dimensions, colors, and other configurations.
Levels.py: Defines the levels with their respective grid configurations.
AIsolver.py: Implements the A* search algorithm to solve the levels.

# Important Classes and Methods
- SokobanGame:

    __init__: Initializes the game environment and settings.
    `load_level()`: Loads and initializes the level from a predefined set.
    `draw_level()`, `draw_player()`: Handle drawing the level and the player.
    `events()`, `handle_keyboard_events()`, `handle_mouse_events()`: Manage user interactions.
    `player_actions()`: Executes the actions that take place when moving the player to a new position on the grid.
    `push_box()`: Attempts to push a box from the player's current position to a new position.
        

- AI:

    `solve_level()`: Implements the A* algorithm to find a solution for the current level.
    `generate_successors()`: Generates possible moves from the current game state.
    `box_heuristic()`: Calculates the heuristic used by the A* algorithm.