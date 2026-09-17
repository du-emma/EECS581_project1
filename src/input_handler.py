# Emma Du, Sneha Thomas

# input_handler.py
# input handler takes the player's physical action (click/flag) and translates it into a call in the game
# game should be using this info

import pygame


class InputHandler:
    def __init__(self, cell_size=40, board_origin=(0, 0), board_size=10):
        self.cell_size = cell_size
        self.board_origin_x, self.board_origin_y = board_origin
        self.board_size = board_size

    def handle_event(self, event):
        # Takes a Pygame event and returns a clean dictionary or None
        if event.type == pygame.MOUSEBUTTONDOWN:
            pixel_x, pixel_y = event.pos

            # Convert screen coordinates into board coordinates by removing
            # the board's top-left offset from the window.
            local_x = pixel_x - self.board_origin_x
            local_y = pixel_y - self.board_origin_y

            if local_x < 0 or local_y < 0:
                return None

            # Convert local pixel coordinates to row/col indices.
            col = local_x // self.cell_size
            row = local_y // self.cell_size

            # Bounds check
            if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                return None

            # Button 1 = Left Click / Tap
            if event.button == 1:
                return {"action": "reveal", "row": row, "col": col}

            # Button 3 = Right Click / Two-finger tap
            elif event.button == 3:
                return {"action": "flag", "row": row, "col": col}

        return None
