import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Minesweeper")

blankCell = pygame.image.load("images/blank_cell.png")
flaggedCell = pygame.image.load("images/flagged_cell.png")
openBombCell = pygame.image.load("images/bomb_cell.png")
openEmptyCell = pygame.image.load("images/open_empty_cell.png")
open1Cell = pygame.image.load("images/open_1_cell.png")
open2Cell = pygame.image.load("images/open_2_cell.png")
open3Cell = pygame.image.load("images/open_3_cell.png")
open4Cell = pygame.image.load("images/open_4_cell.png")
open5Cell = pygame.image.load("images/open_5_cell.png")
open6Cell = pygame.image.load("images/open_6_cell.png")
open7Cell = pygame.image.load("images/open_7_cell.png")
open8Cell = pygame.image.load("images/open_8_cell.png")

bgcolor = (110, 110, 110)
screen.fill(bgcolor)
#pygame.draw.rect(screen, (0, 0, 255), [200, 150, 400, 50], 0)

cells = []

class Cell:
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y
        self.isBomb = False
        self.status = -1
        # -2=flagged; -1=blank; 0=opened empty; 1-8=opened with bomb around; 9=bomb


def main():
    drawGrid()
    pygame.display.flip() # updates the window

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip() # updates the window

    # Quit Pygame
    pygame.quit()



# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
def drawGrid():
    blockSize = 40 # Set the size of the grid block
    for x in range(200, 600, blockSize):
        for y in range(200, 600, blockSize):
            cell = Cell(x, y)
            cells.append(cell)
            screen.blit(blankCell, (x, y))

main()