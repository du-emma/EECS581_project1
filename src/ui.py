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

cells = []

class Cell:
    def __init__(self, x, y, i):
        self.pos = (x, y)
        self.index = i
        self.isBomb = False
        self.status = -1
        # -2=flagged; -1=blank; 0=opened empty; 1-8=opened with bomb around; 9=bomb

    def flag(self):
        if self.status == -2:
            self.status = -1
            screen.blit(blankCell, self.pos)
        elif self.status == -1:
            self.status == -2
            screen.blit(flaggedCell, self.pos)

    #def update(self, mouseButton):
    #    if mouseButton == 1:
    #        match self.status:
    #            case -1: # If blank
    #                screen.blit(blankCell, self.pos)
    #            case 1:
    #                screen.blit(open1Cell, self.pos)
    #            case 2:
    #                screen.blit(open2Cell, self.pos)
    #            case 3:
    #                screen.blit(open3Cell, self.pos)
    #            case 4:
    #                screen.blit(open4Cell, self.pos)
    #            case 5:
    #                screen.blit(open5Cell, self.pos)
    #            case 6:
    #                screen.blit(open6Cell, self.pos)
    #            case 7:
    #                screen.blit(open7Cell, self.pos)
    #            case 8:
    #                screen.blit(open8Cell, self.pos)
    #            case 9: # If bomb
    #                screen.blit(blankCell, self.pos)
    #    elif mouseButton == 3:
    #        if self.status == -2: # If already flagged, unflag
    #            screen.blit(blankCell, self.pos)
    #        elif self.status == -1: # If unflagged, flag
    #            screen.blit(flaggedCell, self.pos)
                


def main():
    drawGrid()
    drawGridLabels()
    
    screen.blit(counter0, leftCounterDigitPos)
    screen.blit(counter0, rightCounterDigitPos)

    pygame.display.flip() # updates the window

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #elif event.type == pygame.MOUSEBUTTONDOWN:
                #cell = findCell(event.pos)
                #if cell:
                    #cell.update(event.button)
        
        pygame.display.flip() # updates the window

    # Quit Pygame
    pygame.quit()



# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
def drawGrid():
    blockSize = 40 # Set the size of the grid block
    index = 0
    for x in range(200, 600, blockSize):
        for y in range(200, 600, blockSize):
            cell = Cell(x, y, index)
            cells.append(cell)
            screen.blit(blankCell, (x, y))
            index += 1

def drawGridLabels():
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

def findCell(mousePos):
    for cell in cells:
        if cell.pos == mousePos:
            return cell


main()