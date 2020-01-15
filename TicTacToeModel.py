"""
    This is the model portion of the Tic Tac Toe application
    created with the pygame library. The game is implemented
    using the MVC model.
"""

import pygame

class TicTacToeModel:
    """
        Each instance of the TacTicToeModel class will have 7 variables
        to represent the game and what is occurring as it is being played:
            self.grid: this is a model of the game itself. The matrix is
                        3x3, and each index in the matrix has a default
                        value of None. Each index will be updated to either
                        'X' or 'O' as the game is played.
            self.boolean_grid: model of the grid that lets the program know
                                whether or not the block at the index of
                                the click can be changed.
            self.player_turn: keeps track of which player's turn it is.
                                Default is Player 1.
            self.bottom_text: this is a string that will be displayed in the
                                bottom box of the game.
            self.game_won: indicates whether the game has been won or not.
                            Default is False.
            self.winner: indicates the winner of the game when game_won is True
            self.player_one_marker: simple character 'X' for player one.
            self.player_two_marker: simple character 'O' for player two.

        This class also contains getter and setter methods for each variable,
        except for the player marker variables.
    """
    def __init__(self):
        self.grid = [[None, None, None],
                     [None, None, None],
                     [None, None, None]]
        self.boolean_grid = [[True, True, True],
                             [True, True, True],
                             [True, True, True]]
        self.player_turn = 1
        self.bottom_text = "Turn: Player " + str(1)
        self.game_won = False
        self.winner = 0
        self.player_one_marker = 'X'
        self.player_two_marker = 'O'

    def get_grid(self):
        return self.grid

    def update_grid(self, row, col, marker):
        assert marker == 'X' or marker == 'O' or marker == None\
            , "Marker must be X or O, or None object."
        self.grid[row][col] = marker

    def get_boolean_grid(self):
        return self.boolean_grid

    def update_boolean_grid(self, row, col, able_to_update):
        assert type(able_to_update) == bool, "Third parameter must be boolean."
        self.boolean_grid[row][col] = able_to_update


    def get_player_turn(self):
        return self.player_turn

    def set_player_turn(self, player_num):
        assert player_num == 1 or player_num == 2, "Number must be 1 or 2."
        self.player_turn = player_num

    def get_bottom_text(self):
        return self.bottom_text

    def set_bottom_text(self, string):
        assert type(string) is str, "Argument must be a string."
        self.bottom_text = string

    def get_game_won(self):
        return self.game_won

    def set_game_won(self, game_status):
        assert type(game_status) is bool, "Argument must be a boolean."
        self.game_won = game_status

    def get_winner(self):
        return self.winner

    def set_winner(self, player_num):
        assert player_num == 1 or player_num == 2 or player_num == 0,\
            "Number must be 0, 1, or 2."
        self.winner = player_num

    def get_player_marker(self, player_num):
        assert player_num == 1 or player_num == 2, "Number must be 1 or 2."
        if player_num == 1:
            return self.player_one_marker
        else:
            return self.player_two_marker