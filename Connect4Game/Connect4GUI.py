import tkinter as tk
from tkinter import messagebox
import Connect4Game as game
import DanielBatyrevAI as DanielAI
import YosefBirnbaumAI as YosefAI
import ShmulyStudentAI as ShmulyAI
import copy

# Instantiate AI strategies
random_choice = DanielAI.RandomStrategy()
yosef_choice = YosefAI.AI_strategy()
shmuli_choice = ShmulyAI.NotRandomStrategy() # default

class Connect4GUI:
    """
    A class to create a graphical interface for the Connect 4 game using Tkinter.

    Attributes
    ----------
    master : tkinter.Tk
        The main Tkinter window for the game.
    game : Connect4Game
        An instance of the Connect4Game class managing the game logic.
    buttons : list
        A list of button widgets for each column to make a move.
    canvas : tkinter.Canvas
        The canvas widget to draw the game board and pieces.

    Methods
    -------
    make_move(column)
        Handles a move made by the player and the AI.
    draw_board()
        Draws the current state of the game board on the canvas.
    """

    def __init__(self, master):
        """
        Initializes the Connect 4 GUI.

        Parameters
        ----------
        master : tkinter.Tk
            The root window of the application.
        """
        self.master = master
        self.master.title("Connect 4")
        self.game = game.Connect4Game()

        # Create button row for column selection
        self.buttons = []
        for col in range(7):
            button = tk.Button(
                master, text=str(col + 1), command=lambda c=col: self.make_move(c)
            )
            button.grid(row=0, column=col)
            self.buttons.append(button)

        # Create canvas for the game board
        self.canvas = tk.Canvas(master, width=7 * 60, height=6 * 60)
        self.canvas.grid(row=1, column=0, columnspan=7)
        self.draw_board()

    def make_move(self, column):
        """
        Handles a move made by the player and the AI.

        Parameters
        ----------
        column : int
            The column index where the player wants to drop a piece.
        """
        
        # Make the player's move
        self.game.make_move(column)
        self.draw_board()

        # Check if the player won
        if self.game.winner is not None:
            winner_text = f"Player {self.game.winner} wins!"
            messagebox.showinfo("Game Over", winner_text)
            self.master.destroy()
            return

        # Make the AI's move - default to shmuli_choice
        game_copy = copy.deepcopy(self.game)
        self.game.make_move(shmuli_choice.strategy(game_copy))
        self.draw_board()

        # Check if the AI won
        if self.game.winner is not None:
            winner_text = f"Player {self.game.winner} wins!"
            messagebox.showinfo("Game Over", winner_text)
            self.master.destroy()

    def draw_board(self):
        """
        Draws the current state of the game board on the canvas.
        """
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the board and pieces
        for row in range(6): # rows
            for col in range(7): # columns
                x0, y0 = col * 60, row * 60
                x1, y1 = x0 + 60, y0 + 60
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

                if self.game.board[row][col] == 1: # index where player one went
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="red", outline="red") # draw red piece
                elif self.game.board[row][col] == 2: # index where player two went
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="yellow", outline="yellow") # draw yellow piece

        # Enable or disable buttons based on the board state
        for col in range(7):
            if self.game.board[0][col] == 0:
                self.buttons[col]["state"] = tk.NORMAL
            else: # don't allow player to move before computer went
                self.buttons[col]["state"] = tk.DISABLED

if __name__ == "__main__":
    # Initialize and start the Connect 4 application
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()
