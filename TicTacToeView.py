"""
    This is the view portion of the Tic Tac Toe application
    created with the pygame library. The game is implemented
    using the MVC model.
"""

import pygame
import TicTacToeModel
import TicTacToeController
import sys

# Create globals for colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Size globals
HEIGHT = 640
WIDTH = 465
SQUARE_HEIGHT = 144
SQUARE_WIDTH = 144
MARGIN = 8

class TicTacToeView:
    """
        Constructor creates the GUI for the game and gives each instance
        of TicTacToeView six variables:
            self.game_window: the window of the GUI
            self.grid: matrix of the surfaces of each box in the game
            self.bottom_text_box: surface that holds text of self.bottom_text
            self.font: font to use in bottom_text_box
            self.bottom_text: string to use to render bottom_text_box
            self.bottom_text_background: surface that self.bottom_text_box
                is centered on.
    """
    def __init__(self):
        model = TicTacToeModel.TicTacToeModel()

        # Create grid for tic tac toe game. Will be 3x3 matrix
        # of rects that are drawn and to be updated.
        self.grid = []
        for i in range(3):
            self.grid.append([])

        # Initialize pygame.
        pygame.init()

        # Set height and width of window.
        self.game_window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Tic Tac Toe")

        # Draw grid for game.
        for row in range(3):
            for column in range(3):
                square = pygame.Surface((SQUARE_WIDTH, SQUARE_HEIGHT))
                square.fill(WHITE)
                square_rect = square.get_rect()
                square_rect = square_rect.move([(MARGIN + SQUARE_WIDTH) * column + MARGIN,
                                            (MARGIN + SQUARE_HEIGHT) * row + MARGIN])
                self.game_window.blit(square, square_rect)

                # Append each surface object to an array so you can update them.
                self.grid[row].append(square)

        # Create bottom box for text to say whose turn it is as well as to contain
        # buttons for restarting and quitting.
        self.font = pygame.font.SysFont('Arial', 25)
        self.bottom_text = model.bottom_text
        self.bottom_text_background = pygame.Surface((SQUARE_WIDTH * 3 + 16, SQUARE_HEIGHT))
        self.bottom_text_background.fill(WHITE)
        self.bottom_text_box = self.font.render(self.bottom_text, True, BLACK, WHITE)
        self.bottom_background_rect = self.bottom_text_background.get_rect()
        self.bottom_background_rect = self.bottom_background_rect.move(8, 480)
        self.game_window.blit(self.bottom_text_background, self.bottom_background_rect)
        bottom_background_center_x = self.bottom_background_rect.centerx
        bottom_background_center_y = self.bottom_background_rect.centery

        # Creating and centering the text surface onto the bottom_text_background
        bottom_rect_text = self.bottom_text_box.get_rect()
        bottom_rect_text_x = bottom_background_center_x - bottom_rect_text.width / 2
        bottom_rect_text_y = bottom_background_center_y - bottom_rect_text.height / 2
        bottom_rect_text = bottom_rect_text.move(bottom_rect_text_x,
                                                 bottom_rect_text_y)
        self.game_window.blit(self.bottom_text_box, bottom_rect_text)