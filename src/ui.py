"""
Module: UI
Description:
    Defines the pygame-based user interface for the Minesweeper game,
    including rendering the board, status text, controls, and reset flow.
Inputs:
    A pygame screen, board manager instance, and current game state.
Outputs:
    Drawn board visuals, status messages, and click-based interactions.
External Sources:
    Stack Overflow was used as a guide for drawing a grid using pygame.
Author:
    Megan Svoren, GitHub Copilot
Created:
    9/14/26
"""
import pygame
from pathlib import Path

try:
    from .board import BoardManager
    from .game import Game
    from .input_handler import InputHandler
except ImportError:  # pragma: no cover
    from board import BoardManager
    from game import Game
    from input_handler import InputHandler


BOARD_ORIGIN = (200, 200)
CELL_SIZE = 40
BOARD_SIZE = 10
MINE_COUNT = 10


class MinesweeperUI:
    # Initialize the UI with the current board, game state, and input handling.
    def __init__(self, screen, board, game):
        self.screen = screen
        self.board = board
        self.game = game
        self.input_handler = InputHandler(
            cell_size=CELL_SIZE,
            board_origin=BOARD_ORIGIN,
            board_size=self.board.ROWS,
        )
        self.bgcolor = (110, 110, 110)
        self.assets = self._load_assets()

    # Load all visual assets for covered, flagged, empty, and numbered cells.
    def _load_assets(self):
        base_dir = Path(__file__).resolve().parent.parent
        image_dir = base_dir / "images"
        assets = {}
        names = {
            "blank": "blank_cell.png",
            "flagged": "flagged_cell.png",
            "bomb": "bomb_cell.png",
            "empty": "open_empty_cell.png",
            "1": "open_1_cell.png",
            "2": "open_2_cell.png",
            "3": "open_3_cell.png",
            "4": "open_4_cell.png",
            "5": "open_5_cell.png",
            "6": "open_6_cell.png",
            "7": "open_7_cell.png",
            "8": "open_8_cell.png",
        }

        for key, filename in names.items():
            path = image_dir / filename
            if path.exists():
                assets[key] = pygame.image.load(str(path)).convert_alpha()
            else:
                surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                surface.fill((200, 200, 200))
                if key == "flagged":
                    surface.fill((255, 0, 0))
                elif key == "bomb":
                    surface.fill((0, 0, 0))
                elif key == "empty":
                    surface.fill((220, 220, 220))
                elif key in {"1", "2", "3", "4", "5", "6", "7", "8"}:
                    surface.fill((180, 180, 180))
                assets[key] = surface

        return assets

    # Fill the screen and draw the empty board background before cells are painted.
    def draw_grid(self):
        self.screen.fill(self.bgcolor)
        for row in range(self.board.ROWS):
            for col in range(self.board.COLS):
                x = BOARD_ORIGIN[0] + col * CELL_SIZE
                y = BOARD_ORIGIN[1] + row * CELL_SIZE
                self.screen.blit(self.assets["blank"], (x, y))

    # Convert the game state into a user-facing status message.
    def get_status_text(self):
        status = self.game.getStatus()
        if status == "WON":
            return "Game won!"
        if status == "LOST":
            return "Game lost"
        return "Now playing..."

    # Draw the current game status above the board.
    def draw_status(self):
        font = pygame.font.SysFont(None, 48)
        text = self.get_status_text()
        text_surface = font.render(text, True, (255, 255, 255), self.bgcolor)
        x = BOARD_ORIGIN[0]
        y = BOARD_ORIGIN[1] - 50
        rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, rect)

    # Draw the row and column labels around the board edges.
    def draw_labels(self):
        rows = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        label_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 40)

        for i, item in enumerate(rows):
            row_label = font.render(item, True, label_color, self.bgcolor)
            self.screen.blit(row_label, (180 - row_label.get_width() // 2, 207 + i * 40))

        for j, item in enumerate(cols):
            col_label = font.render(item, True, label_color, self.bgcolor)
            self.screen.blit(col_label, (220 + j * 40 - col_label.get_width() // 2, 605))

    # Draw the remaining flag counter at the top of the board area.
    def draw_counter(self):
        digit_map = {}
        for digit in range(10):
            filename = f"counter_{digit}.png"
            path = Path(__file__).resolve().parent.parent / "images" / filename
            if path.exists():
                digit_map[digit] = pygame.image.load(str(path)).convert_alpha()
            else:
                surf = pygame.Surface((20, 30))
                surf.fill((200, 200, 200))
                digit_map[digit] = surf

        remaining = max(self.game.remainingFlags(), 0)
        right_digit = remaining % 10
        left_digit = remaining // 10

        self.screen.blit(digit_map[left_digit], (519, 120))
        self.screen.blit(digit_map[right_digit], (559, 120))

    # Show a restart button only after the player loses the game.
    def draw_new_game_button(self):
        if self.game.getStatus() != "LOST":
            return

        button_rect = pygame.Rect(300, 650, 200, 60)
        pygame.draw.rect(self.screen, (70, 70, 70), button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)

        font = pygame.font.SysFont(None, 36)
        text = font.render("New Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        return button_rect

    # Render one cell based on its covered, flagged, mine, and number state.
    def draw_cell(self, row, col):
        cell = self.board.getCell(row, col)
        x = BOARD_ORIGIN[0] + col * CELL_SIZE
        y = BOARD_ORIGIN[1] + row * CELL_SIZE

        if cell.isFlagged():
            self.screen.blit(self.assets["flagged"], (x, y))
            return

        if not cell.isUncovered():
            self.screen.blit(self.assets["blank"], (x, y))
            return

        if cell.hasMine():
            self.screen.blit(self.assets["bomb"], (x, y))
            return

        count = cell.getAdjacentMines()
        if count == 0:
            self.screen.blit(self.assets["empty"], (x, y))
        else:
            self.screen.blit(self.assets[str(count)], (x, y))

    # Repaint the entire screen from the current game and board state.
    def render(self):
        self.draw_grid()
        self.draw_status()
        for row in range(self.board.ROWS):
            for col in range(self.board.COLS):
                self.draw_cell(row, col)
        self.draw_labels()
        self.draw_counter()
        self.draw_new_game_button()
        pygame.display.flip()

    # Create a fresh board and game instance for a new round.
    def reset_game(self):
        self.board = BoardManager()
        self.game = Game(self.board, MINE_COUNT)
        self.input_handler = InputHandler(
            cell_size=CELL_SIZE,
            board_origin=BOARD_ORIGIN,
            board_size=self.board.ROWS,
        )
        self.render()

    # Handle mouse input, including the restart button after a loss.
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game.getStatus() == "LOST":
                button_rect = self.draw_new_game_button()
                if button_rect is not None and button_rect.collidepoint(event.pos):
                    self.reset_game()
                    return

        action = self.input_handler.handle_event(event)
        if action is None:
            return

        row = action["row"]
        col = action["col"]

        if action["action"] == "uncover":
            self.game.uncover(row, col)
        elif action["action"] == "flag":
            self.game.toggleFlag(row, col)

        self.render()


# Launch the pygame window and start the Minesweeper game loop.
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Minesweeper")

    board = BoardManager()
    game = Game(board, MINE_COUNT)
    ui = MinesweeperUI(screen, board, game)
    ui.render()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                ui.handle_event(event)

    pygame.quit()


if __name__ == "__main__":
    main()

