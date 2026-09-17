import pygame

try:
    from .board import BoardManager
    from .game import Game
except ImportError:  # pragma: no cover
    from board import BoardManager
    from game import Game


# Initialize Pygame
pygame.init()

board = BoardManager()
game = Game(board, 10)

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
counter0 = pygame.image.load("images/counter_0.png")
counter1 = pygame.image.load("images/counter_1.png")
counter2 = pygame.image.load("images/counter_2.png")
counter3 = pygame.image.load("images/counter_3.png")
counter4 = pygame.image.load("images/counter_4.png")
counter5 = pygame.image.load("images/counter_5.png")
counter6 = pygame.image.load("images/counter_6.png")
counter7 = pygame.image.load("images/counter_7.png")
counter8 = pygame.image.load("images/counter_8.png")
counter9 = pygame.image.load("images/counter_9.png")

leftCounterDigitPos = (519, 120)
rightCounterDigitPos = (559, 120)

bgcolor = (110, 110, 110)
screen.fill(bgcolor)

grid = board.getBoard()

class uiManager:
    def __init__(self):
        self.drawGrid()
        self.drawGridLabels()
        self.updateCounter()

    def setCellStatus(self, cell):
        cellPos = self.findCellPos(cell)

        if cell.getState() == 0: # covered
            screen.blit(blankCell, cellPos)
        elif cell.getState() == 1: # flagged
            screen.blit(flaggedCell, cellPos)
        elif cell.getState() == 2: # uncovered
            if cell.hasMine():
                screen.blit(openBombCell, cellPos)
                self.triggerLoss()
            else:
                numAdjacentMines = cell.getAdjacentMines()
                match numAdjacentMines:
                    case 0:
                        screen.blit(openEmptyCell, cellPos)
                    case 1:
                        screen.blit(open1Cell, cellPos)
                    case 2:
                        screen.blit(open2Cell, cellPos)
                    case 3:
                        screen.blit(open3Cell, cellPos)
                    case 4:
                        screen.blit(open4Cell, cellPos)
                    case 5:
                        screen.blit(open5Cell, cellPos)
                    case 6:
                        screen.blit(open6Cell, cellPos)
                    case 7:
                        screen.blit(open7Cell, cellPos)
                    case 8:
                        screen.blit(open8Cell, cellPos)
        self.updateCounter()
        pygame.display.flip() # updates the window

    def updateCounter(self):
        number = game.remainingFlags()
        rightCounterDigit = number % 10
        leftCounterDigit = (number - rightCounterDigit) / 10

        match rightCounterDigit:
            case 0:
                screen.blit(counter0, rightCounterDigitPos)
            case 1:
                screen.blit(counter1, rightCounterDigitPos)
            case 2:
                screen.blit(counter2, rightCounterDigitPos)
            case 3:
                screen.blit(counter3, rightCounterDigitPos)
            case 4:
                screen.blit(counter4, rightCounterDigitPos)
            case 5:
                screen.blit(counter5, rightCounterDigitPos)
            case 6:
                screen.blit(counter6, rightCounterDigitPos)
            case 7:
                screen.blit(counter7, rightCounterDigitPos)
            case 8:
                screen.blit(counter8, rightCounterDigitPos)
            case 9:
                screen.blit(counter9, rightCounterDigitPos)
        
        match leftCounterDigit:
            case 0:
                screen.blit(counter0, leftCounterDigitPos)
            case 1:
                screen.blit(counter1, leftCounterDigitPos)
            case 2:
                screen.blit(counter2, leftCounterDigitPos)
            case 3:
                screen.blit(counter3, leftCounterDigitPos)
            case 4:
                screen.blit(counter4, leftCounterDigitPos)
            case 5:
                screen.blit(counter5, leftCounterDigitPos)
            case 6:
                screen.blit(counter6, leftCounterDigitPos)
            case 7:
                screen.blit(counter7, leftCounterDigitPos)
            case 8:
                screen.blit(counter8, leftCounterDigitPos)
            case 9:
                screen.blit(counter9, leftCounterDigitPos)
        
        pygame.display.flip() # updates the window

    def triggerLoss(self):

        # Quit Pygame
        pygame.quit()
        return

    def triggerWin(self):
        return

    def findCellPos(self, cell):
        for i, row in enumerate(grid):
            if cell in row:
                return (i, row.index(cell))

    # https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    def drawGrid(self):
        #blockSize = 40px
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                screen.blit(blankCell, (200 + 40*x, 200 + 40*y))

    def drawGridLabels(self):
        rows = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        label_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 40)

        i = 0
        for item in rows:
            row_image = font.render(item, True, label_color, bgcolor)
            screen.blit(row_image, (180 - (row_image.get_width() / 2), 207 + i))
            i += 40

        j = 0
        for item in cols:
            col_image = font.render(item, True, label_color, bgcolor)
            screen.blit(col_image, (220 + j - (col_image.get_width() / 2), 605))
            j += 40


def main():
    ui = uiManager()
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()

