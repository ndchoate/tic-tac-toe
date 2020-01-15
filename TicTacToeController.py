"""
    This is the controller portion of the Tic Tac Toe application
    created with the pygame library. The game is implemented
    using the MVC model.
"""

import pygame
import TicTacToeView
import TicTacToeModel

# Create global constants for colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Size globals
HEIGHT = 640
WIDTH = 465
SQUARE_HEIGHT = 144
SQUARE_WIDTH = 144
MARGIN = 8

class TicTacToeController:
    def __init__(self, view, model):
        self.view = view
        self.model = model


    """
        Method to update the text in the text box for the GUI. Very messy,
        needs revision if time allows.
    """
    def update_bottom_text(self, view, model):
        view.bottom_text_box = view.font.render(model.bottom_text, True, BLACK, WHITE)
        bottom_text_background = pygame.Surface((TicTacToeView.SQUARE_WIDTH * 3 + 16,
                                                 TicTacToeView.SQUARE_HEIGHT))
        bottom_text_background.fill(TicTacToeView.WHITE)
        bottom_background_rect = bottom_text_background.get_rect()
        bottom_background_rect = bottom_background_rect.move(8, 480)
        bottom_background_center_x = bottom_background_rect.centerx
        bottom_background_center_y = bottom_background_rect.centery
        bottom_rect_text = view.bottom_text_box.get_rect()
        bottom_rect_text_x = bottom_background_center_x - bottom_rect_text.width / 2
        bottom_rect_text_y = bottom_background_center_y - bottom_rect_text.height / 2
        bottom_rect_text = bottom_rect_text.move(bottom_rect_text_x,
                                                 bottom_rect_text_y)
        view.game_window.blit(view.bottom_text_box, bottom_rect_text)


    """
        Update GUI to match model's grid matrix.
    """
    def update_grid_view(self, view, model):
        model_grid = model.get_grid()
        view_grid = view.grid
        model_boolean_grid = model.get_boolean_grid()

        for row in range(3):
            for col in range(3):
                block_to_change = view_grid[row][col]
                mark_at_pos = model_grid[row][col]
                bool_at_pos = model_boolean_grid[row][col]


                if bool_at_pos:
                    # Fill block in view grid with plain white.
                    if mark_at_pos == None:
                        block_to_change.fill(WHITE)
                        square_rect = block_to_change.get_rect()
                        square_rect = square_rect.move([(MARGIN + SQUARE_WIDTH) * col + MARGIN,
                                                       (MARGIN + SQUARE_HEIGHT) * row + MARGIN])
                        view.game_window.blit(block_to_change, square_rect)

                    # Fill block in view with X_marker.png
                    elif mark_at_pos == 'X':
                        block_to_change.blit(pygame.image.load("X_marker.png"),
                                            block_to_change.get_rect())
                        square_rect = block_to_change.get_rect()
                        square_rect = square_rect.move([(MARGIN + SQUARE_WIDTH) * col + MARGIN,
                                                        (MARGIN + SQUARE_HEIGHT) * row + MARGIN])
                        view.game_window.blit(block_to_change, square_rect)

                        # Set bool at block's position (model.boolean_grid[row][col]) to
                        # False so it cannot be changed again.
                        model.update_boolean_grid(row, col, False)
                    # Fill block in view with O_marker.png
                    else:
                        block_to_change.blit(pygame.image.load("O_marker.png"),
                                            block_to_change.get_rect())
                        square_rect = block_to_change.get_rect()
                        square_rect = square_rect.move([(MARGIN + SQUARE_WIDTH) * col + MARGIN,
                                                        (MARGIN + SQUARE_HEIGHT) * row + MARGIN])
                        view.game_window.blit(block_to_change, square_rect)

                        # Set bool at block's position (model.boolean_grid[row][col]) to
                        # False so it cannot be changed again.
                        model.update_boolean_grid(row, col, False)


    """
        Listen for click events. Returns boolean of whether user
        clicked the close button.
    """
    def process_click_event(self, view, model):
        exit_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_clicked = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get position of mouse click.
                position = pygame.mouse.get_pos()
                # Convert x/y coords on screen to grid coords
                column = position[0] // (TicTacToeView.SQUARE_WIDTH +
                                    TicTacToeView.MARGIN)
                row = position[1] // (TicTacToeView.SQUARE_HEIGHT +
                                      TicTacToeView.MARGIN)

                # Set grid model's location that was clicked to
                # current player's marker.
                model_grid = model.get_grid()
                model_boolean_grid = model.get_boolean_grid()
                player = model.get_player_turn()
                player_marker = model.get_player_marker(player)

                # Check game for a winner or a tie.
                game_over = self.check_for_winner(view, model)
                game_tied = self.check_for_tie(view, model)

                # If clicked below grid, either continue to next iteration or restart game.
                if row > 2 or column > 2:
                    if game_over or game_tied:
                        self.restart_game(view, model)
                    else:
                        continue
                # If clicked on block in grid, update grid in model
                # if that block in the grid is able to be changed.
                else:
                    if not game_over and model_boolean_grid[row][column]:
                        self.switch_player_turn(model)
                        model_grid[row][column] = player_marker
                        model.update_grid(row, column, player_marker)


                # Check again if game is over or tied, change bottom text according to result.
                game_over = self.check_for_winner(view, model)
                game_tied = self.check_for_tie(view, model)
                if game_tied:
                    self.update_bottom_text(view, model)
                elif not game_over:
                    model.set_bottom_text("Turn: Player " + str(model.get_player_turn()))
                else:
                    model.set_bottom_text("Game Over. Player " + str(model.get_winner()) +
                                            " wins. Click here to restart.")

                self.update_bottom_text(view, model)

        return exit_clicked

    """
        Changes the turn to the next player in model.
    """
    def switch_player_turn(self, model):
        player_turn = model.get_player_turn()
        if player_turn == 1:
            player_turn = 2
        else:
            player_turn = 1

        model.set_player_turn(player_turn)

    """
        Checks model for a winner. Returns boolean,
        True if there's a winner and False if not.
        Also changes model.winner attribute.
    """
    def check_for_winner(self, view, model):
        model_grid = model.get_grid()
        p1_marker = model.get_player_marker(1)
        p2_marker = model.get_player_marker(2)


        # Check all rows for winner
        for row in range(3):
            p1_three_in_row = (model_grid[row][0] == p1_marker and
                               model_grid[row][1] == p1_marker and
                               model_grid[row][2] == p1_marker)
            p2_three_in_row = (model_grid[row][0] == p2_marker and
                               model_grid[row][1] == p2_marker and
                               model_grid[row][2] == p2_marker)
            if p1_three_in_row:
                model.set_winner(1)
                model.set_bottom_text("Game Over. Player 1 wins. Click here to restart.")
                return True

            if p2_three_in_row:
                model.set_winner(2)
                model.set_bottom_text("Game Over. Player 2 wins. Click here to restart.")
                return True

        # Check all columns for winner.
        for col in range(3):
            p1_three_in_col = (model_grid[0][col] == p1_marker and
                               model_grid[1][col] == p1_marker and
                               model_grid[2][col] == p1_marker)
            p2_three_in_col = (model_grid[0][col] == p2_marker and
                               model_grid[1][col] == p2_marker and
                               model_grid[2][col] == p2_marker)

            if p1_three_in_col:
                model.set_winner(1)
                model.set_bottom_text("Game Over. Player 1 wins. Click here to restart.")
                return True

            if p2_three_in_col:
                model.set_winner(2)
                model.set_bottom_text("Game Over. Player 2 wins. Click here to restart.")
                return True

        # Check diagonals for winner.
        p1_three_in_diag1 = (model_grid[0][0] == p1_marker and
                             model_grid[1][1] == p1_marker and
                             model_grid[2][2] == p1_marker)
        p2_three_in_diag1 = (model_grid[0][0] == p2_marker and
                             model_grid[1][1] == p2_marker and
                             model_grid[2][2] == p2_marker)
        p1_three_in_diag2 = (model_grid[0][2] == p1_marker and
                             model_grid[1][1] == p1_marker and
                             model_grid[2][0] == p1_marker)
        p2_three_in_diag2 = (model_grid[0][2] == p2_marker and
                             model_grid[1][1] == p2_marker and
                             model_grid[2][0] == p2_marker)
        if p1_three_in_diag1 or p1_three_in_diag2:
            model.set_winner(1)
            model.set_bottom_text("Game Over. Player 1 wins. Click here to restart.")
            return True
        if p2_three_in_diag1 or p2_three_in_diag2:
            model.set_winner(2)
            model.set_bottom_text("Game Over. Player 2 wins. Click here to restart.")
            return True

        return False

    """
        Checks to see if the game is tied. Returns True if it is, False if not.
    """
    def check_for_tie(self, view, model):
        has_winner = self.check_for_winner(view, model)
        has_empty_block = False
        game_tied = False
        model_grid = model.get_grid()

        for row in range(3):
            for col in range(3):
                if model_grid[row][col] == None:
                    has_empty_block = True
                    break

        if not has_winner and not has_empty_block:
            game_tied = True
            model.set_bottom_text("Game is tied. Click here to restart.")
        return game_tied

    """
        Sets model and view objects back to default settings,
        as shown in their constructors.
    """
    def restart_game(self, view, model):
        for row in range(3):
            for col in range(3):
                model.update_grid(row, col, None)
                model.update_boolean_grid(row, col, True)

        model.set_bottom_text("Turn: Player " + str(1))
        model.set_player_turn(1)
        model.set_game_won(False)
        model.set_winner(0)
        view.bottom_text_background = pygame.Surface((SQUARE_WIDTH * 3 + 16, SQUARE_HEIGHT))
        view.bottom_text_background.fill(WHITE)
        view.bottom_background_rect = view.bottom_text_background.get_rect()
        view.bottom_background_rect = view.bottom_background_rect.move(8, 480)
        view.game_window.blit(view.bottom_text_background, view.bottom_background_rect)
