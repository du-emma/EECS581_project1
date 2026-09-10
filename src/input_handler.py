# Emma Du, Sneha Thomas

# input_handler.py
import pygame

class InputHandler:
    def __init__(self, cell_size=40):
        self.cell_size = cell_size

    def handle_event(self, event):
        """
        Takes a Pygame event and returns a clean dictionary or None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pixel_x, pixel_y = event.pos
            col = pixel_x // self.cell_size
            row = pixel_y // self.cell_size

            # Button 1 = Left Click / Tap
            if event.button == 1:
                return {"action": "reveal", "row": row, "col": col}

            # Button 3 = Right Click / Two-finger tap
            elif event.button == 3:
                return {"action": "flag", "row": row, "col": col}

        return None