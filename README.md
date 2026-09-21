# EECS581 Project 1: Minesweeper

This project is a Python implementation of the Minesweeper game. It includes a game model, board logic, input handling, and basic user interface.

## Project Overview

The application includes:
- a 10x10 Minesweeper board
- mine placement logic
- adjacent mine counting
- cell state tracking (covered, flagged, uncovered)
- basic game win/loss logic
- pygame-based UI rendering

## Repository Structure

- `src/board.py` – manages the board and cell grid
- `src/cell.py` – stores cell properties and state
- `src/game.py` – contains the game rules and win/loss conditions
- `src/input_handler.py` – converts mouse input into board actions
- `src/ui.py` – renders the board and handles interaction with the game
- `src/main.py` – entry point for the program
- `tests/` – project test files for validating game logic

## Requirements

This project requires:
- Python 3
- pygame

Install dependencies with:

```bash
pip install pygame
```

## How to Run

From the project root, run:

```bash
python -m src.main
```

If the package import does not work in your environment, you can also run:

```bash
python src/main.py
```

## How to Play

- Left click: uncover a cell
- Right click: place/remove a flag
- The first clicked cell should be safe
- Numbers display how many mines are adjacent to a cell
- Revealing all non-mine cells wins the game
- Revealing a mine ends the game

## Authors for this project:

- Emma Du, Serom Kim, Megan Svoren, Sneha Thomas, Ellie Thach, Jana Frady, Arpa Das, Emma Roy
