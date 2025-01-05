
from abc import (ABC, abstractmethod)


class Connect4GameStrategy(ABC):
    """
    An abstract base class to define the strategy interface for Connect 4 AI players.

    Methods
    -------
    strategy(game_safety_copy)
        Abstract method to implement the AI's move strategy.
    """
    
    def __init__(self):
        """
        Initializes the Connect4GameStrategy base class.
        """
        ...

    @abstractmethod
    def strategy(self, game_safety_copy):
        """
        Defines the strategy for making a move in the game.

        Parameters
        ----------
        game_safety_copy : Connect4Game
            A copy of the current game state, ensuring the AI cannot modify the original state.

        Returns
        -------
        int
            The column index where the AI decides to make a move.
        """
        ...


class Connect4Game:
    """
    A class to handle the core game logic for Connect 4.

    Attributes
    ----------
    board : list of list of int
        A 6x7 matrix representing the game board, where 0 indicates an empty slot,
        1 indicates Player 1's piece, and 2 indicates Player 2's piece.
    current_player : int
        The current player (1 for Player 1, 2 for Player 2).
    winner : int or None
        The winner of the game, or None if there is no winner yet.

    Methods
    -------
    is_valid_move(column)
        Checks if a move in the specified column is valid.
    make_move(column)
        Makes a move for the current player in the specified column.
    check_winner(row, col)
        Checks if the current player has won after placing a piece.
    check_line(row, col, dr, dc)
        Checks a line in a specific direction for a winning streak of four.
    """
    def __init__(self):
        """
        Initializes the Connect 4 game board and sets up the game state.
        """
        self.board = [[0] * 7 for _ in range(6)]  # 6 rows and 7 columns
        self.current_player = 1  # Player 1 starts
        self.winner = None  # No winner initially

    def is_valid_move(self, column):
        """
        Checks if a move in the specified column is valid.

        Parameters
        ----------
        column : int
            The column index to check.

        Returns
        -------
        bool
            True if the move is valid, False otherwise.
        """
        if not (0 <= column < 7):
            return False  # Column index is out of range
        return self.board[0][column] == 0  # Check if the column is not full

    def make_move(self, column):
        """
        Makes a move for the current player in the specified column.

        Parameters
        ----------
        column : int
            The column index where the player wants to drop a piece.
        """
        if not self.is_valid_move(column) or self.winner is not None:
            return  # Invalid move or game already won

        # Place the piece in the lowest available row in the column
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                if self.check_winner(row, column):
                    self.winner = self.current_player  # Declare winner
                else:
                    self.current_player = 3 - self.current_player  # Switch player
                return


    def check_winner(self, row, col):
        """
        Checks if the current player has won after placing a piece.

        Parameters
        ----------
        row : int
            The row index of the last move.
        col : int
            The column index of the last move.

        Returns
        -------
        bool
            True if the current player has won, False otherwise.
        """
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, vertical, diagonal directions
        results = [self.check_line(row, col, dr, dc) for dr, dc in directions]
        return any(results)

    def check_line(self, row, col, dr, dc):
        """
        Checks a line in a specific direction for a winning streak of four.

        Parameters
        ----------
        row : int
            Starting row index.
        col : int
            Starting column index.
        dr : int
            Row direction increment.
        dc : int
            Column direction increment.

        Returns
        -------
        bool
            True if a winning streak of four is found, False otherwise.
        """
        count = 0
        row = row - dr * 3  # Move back 3 steps to check full range
        col = col - dc * 3
        for _ in range(7):  # Check 7 positions in the line
            if 0 <= row < 6 and 0 <= col < 7 and self.board[row][col] == self.current_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += dr
            col += dc

        return False
