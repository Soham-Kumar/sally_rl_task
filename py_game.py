import sys
import pygame

pygame.init()

# set up the window
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("RL Task for Sally")

# set up the board
board = pygame.Surface((600, 600))
board.fill((255, 206, 158))

# draw the board
for x in range(3):
    for y in range(3):
        if (x + y) % 2 == 0:
            pygame.draw.rect(board, (150, 150, 0), (x * 200, y * 200, 200, 200))
        else:
            pygame.draw.rect(board, (210, 180, 140), (x * 200, y * 200, 200, 200))


# add the board to the screen
screen.blit(board, (0, 0))

pygame.display.flip()


# Piece class whose instances will represent each piece on the board.
class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def draw(self, surface):
        try:
            img = pygame.image.load(f"sally/sally_rl_task/{self.color}.png")
        except pygame.error as e:
            print("Error loading image:", e)
        img_small = pygame.transform.scale(img, (180, 180))
        surface.blit(img_small, (self.x * 200 + 10, self.y * 200 + 10))

    def can_move_to(self, x, y, pieces):
        # Check if the piece can move to the specified position
        if self.color == "black":
            # Black pieces can only move downwards (increase in y position)
            if y > self.y and abs(x - self.x) == 0:
                # Check if the destination block is occupied by another piece
                for piece in pieces:
                    if piece != self and piece.x == x and piece.y == y:
                        return False
                # Check if there is a white piece blocking the path
                for piece in pieces:
                    if piece.color == "white" and piece.x == self.x and self.y < piece.y < y:
                        return False
                return True
        elif self.color == "white":
            # White pieces can only move upwards (decrease in y position)
            if y < self.y and abs(x - self.x) == 0:
                # Check if the destination block is occupied by another piece
                for piece in pieces:
                    if piece != self and piece.x == x and piece.y == y:
                        return False
                # Check if there is a black piece blocking the path
                for piece in pieces:
                    if piece.color == "black" and piece.x == self.x and y < piece.y < self.y:
                        return False
                return True
        return False


# set up the pieces
pieces = []
for i in range(3):
    pieces.append(Piece("black", i, 0))
    pieces.append(Piece("white", i, 2))
print(pieces)

# draw the pieces
for piece in pieces:
    piece.draw(board)


# main loop
selected_piece = None
dragging = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not dragging:
                # get the position of the click
                pos = pygame.mouse.get_pos()

                # convert the position to board coordinates
                x = (pos[0]) // 200
                y = (pos[1]) // 200

                # find the piece at the clicked position
                for piece in pieces:
                    if piece.x == x and piece.y == y:
                        selected_piece = piece
                        dragging = True
                        break
            else:
                # stop dragging the piece
                dragging = False
                selected_piece = None

        if event.type == pygame.MOUSEMOTION and dragging:
            # update the position of the selected piece while dragging
            pos = pygame.mouse.get_pos()
            x = (pos[0]) // 200
            y = (pos[1]) // 200

            # move the piece only if the destination block is valid
            if selected_piece.can_move_to(x, y, pieces):
                selected_piece.x = x
                selected_piece.y = y

    # redraw the board and pieces
    board.fill((255, 206, 158))
    for x in range(3):
        for y in range(3):
            if (x + y) % 2 == 0:
                pygame.draw.rect(board, (0, 150, 0), (x * 200, y * 200, 200, 200))
            else:
                pygame.draw.rect(board, (210, 180, 140), (x * 200, y * 200, 200, 200))

    for piece in pieces:
        piece.draw(board)

    # add the board to the screen
    screen.blit(board, (0, 0))

    # update the display
    pygame.display.update()
