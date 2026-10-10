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
    ChatGPT was used to assist with integrating the AI difficulty controls
    and Interactive/Auto Solve modes into the Pygame UI.
Author:
    Megan Svoren, GitHub Copilot
Modified by:
    Ever Armenta - AI UI integration
Created:
    9/14/26
Modified:
    10/09/26
"""
import pygame
from pathlib import Path

try:
    from .board import BoardManager
    from .game import Game
    from .input_handler import InputHandler
    from .ai_solver import AISolver
except ImportError:  # pragma: no cover
    from board import BoardManager
    from game import Game
    from input_handler import InputHandler
    from ai_solver import AISolver


BOARD_ORIGIN = (200, 200)
CELL_SIZE = 40
BOARD_SIZE = 10
MINE_COUNT = 10

AI_AUTO_EVENT = pygame.USEREVENT + 1
AI_AUTO_DELAY_MS = 300


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

        self.ai_solver = AISolver(self.game)
        self.ai_difficulty = "Medium"
        self.ai_mode = "Interactive"
        self.auto_running = False

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

    # Make one AI move using the selected difficulty.
    def run_ai_move(self):
        if self.game.getStatus() != "IN_PROGRESS":
            return

        if self.ai_difficulty == "Medium":
            self.ai_solver.medium_move()

        elif self.ai_difficulty == "Hard":
            self.ai_solver.hard_move()

        elif self.ai_difficulty == "Easy":
            # Easy automatically becomes usable when Viren adds easy_move()
            # to the shared AISolver class.
            if hasattr(self.ai_solver, "easy_move"):
                self.ai_solver.easy_move()

    # Draw the AI difficulty and operating-mode controls.
    def draw_ai_controls(self):
        font = pygame.font.SysFont(None, 24)

        difficulty_buttons = {
            "Easy": pygame.Rect(205, 635, 110, 38),
            "Medium": pygame.Rect(345, 635, 110, 38),
            "Hard": pygame.Rect(485, 635, 110, 38),
        }

        mode_buttons = {
            "Interactive": pygame.Rect(245, 685, 140, 38),
            "Auto Solve": pygame.Rect(415, 685, 140, 38),
        }

        easy_available = hasattr(self.ai_solver, "easy_move")

        for label, rect in difficulty_buttons.items():
            enabled = label != "Easy" or easy_available

            if not enabled:
                fill = (50, 50, 50)
                text_color = (150, 150, 150)
            elif label == self.ai_difficulty:
                fill = (100, 100, 100)
                text_color = (255, 255, 255)
            else:
                fill = (70, 70, 70)
                text_color = (255, 255, 255)

            pygame.draw.rect(self.screen, fill, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            label_surface = font.render(label, True, text_color)
            self.screen.blit(
                label_surface,
                label_surface.get_rect(center=rect.center),
            )

        for label, rect in mode_buttons.items():
            selected = label == self.ai_mode
            fill = (100, 100, 100) if selected else (70, 70, 70)

            pygame.draw.rect(self.screen, fill, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            label_surface = font.render(label, True, (255, 255, 255))
            self.screen.blit(
                label_surface,
                label_surface.get_rect(center=rect.center),
            )

        start_button = None

        if self.ai_mode == "Auto Solve":
            start_button = pygame.Rect(300, 735, 200, 38)
            pygame.draw.rect(self.screen, (70, 70, 70), start_button)
            pygame.draw.rect(self.screen, (255, 255, 255), start_button, 2)

            label = "Stop AI" if self.auto_running else "Start AI"
            label_surface = font.render(label, True, (255, 255, 255))
            self.screen.blit(
                label_surface,
                label_surface.get_rect(center=start_button.center),
            )

        return difficulty_buttons, mode_buttons, start_button

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

        if self.game.getStatus() == "IN_PROGRESS":
            self.draw_ai_controls()

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
        self.ai_solver = AISolver(self.game)
        self.auto_running = False
        pygame.time.set_timer(AI_AUTO_EVENT, 0)
        self.render()

    # Handle player input and AI controls.
    def handle_event(self, event):
        # Auto Solve makes one AI move every timer tick.
        if event.type == AI_AUTO_EVENT:
            if self.auto_running and self.game.getStatus() == "IN_PROGRESS":
                self.run_ai_move()

                if self.game.getStatus() != "IN_PROGRESS":
                    self.auto_running = False
                    pygame.time.set_timer(AI_AUTO_EVENT, 0)

                self.render()

            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game.getStatus() == "LOST":
                button_rect = self.draw_new_game_button()

                if button_rect is not None and button_rect.collidepoint(event.pos):
                    self.reset_game()
                    return

            if self.game.getStatus() == "IN_PROGRESS":
                difficulty_buttons, mode_buttons, start_button = (
                    self.draw_ai_controls()
                )

                # Difficulty selection.
                for label, rect in difficulty_buttons.items():
                    if rect.collidepoint(event.pos):
                        if label == "Easy" and not hasattr(
                            self.ai_solver, "easy_move"
                        ):
                            return

                        self.ai_difficulty = label
                        self.render()
                        return

                # Interactive / Auto Solve selection.
                for label, rect in mode_buttons.items():
                    if rect.collidepoint(event.pos):
                        self.ai_mode = label

                        if label == "Interactive":
                            self.auto_running = False
                            pygame.time.set_timer(AI_AUTO_EVENT, 0)

                        self.render()
                        return

                # Start or stop automatic solving.
                if (
                    self.ai_mode == "Auto Solve"
                    and start_button is not None
                    and start_button.collidepoint(event.pos)
                ):
                    self.auto_running = not self.auto_running

                    pygame.time.set_timer(
                        AI_AUTO_EVENT,
                        AI_AUTO_DELAY_MS if self.auto_running else 0,
                    )

                    self.render()
                    return

        # Ignore normal board clicks while Auto Solve is actively running.
        if self.auto_running:
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

        # In Interactive mode, every player action is followed by one AI turn.
        if (
            self.ai_mode == "Interactive"
            and self.game.getStatus() == "IN_PROGRESS"
        ):
            self.run_ai_move()

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

