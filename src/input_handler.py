# Emma Du, Sneha Thomas

# input_handler.py
# input handler takes the player's physical action (click/flag) and translates it into a call in the game
# game should be using this info

import pygame

class InputHandler:
    def __init__(self, cell_size=40):
        self.cell_size = cell_size

    def handle_event(self, event):
        # Takes a Pygame event and returns a clean dictionary or None
        if event.type == pygame.MOUSEBUTTONDOWN:
            pixel_x, pixel_y = event.pos
            # convert pixels to board col n row
            col = pixel_x // self.cell_size
            row = pixel_y // self.cell_size
            
            #bounds check
            if not (0 <= row < 10 and 0 <= col < 10):
                return None

            # Button 1 = Left Click / Tap
            if event.button == 1:
                return {"action": "reveal", "row": row, "col": col}

            # Button 3 = Right Click / Two-finger tap
            elif event.button == 3:
                return {"action": "flag", "row": row, "col": col}

        return None
