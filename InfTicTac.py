"""
Created by Avi Serebrenik
An infinite tic-tac-toe game built with Python and Tkinter.
The base tic-tac-toe game was found in the following guide: https://realpython.com/tic-tac-toe-python/
"""

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple):   #player class
    label: str  #store x or o
    color:str   #color for player indentification

class Move(NamedTuple):     #class for each move
    row:int     #coordinates of move
    col:int
    label:str = ""  #whether move is legal

BOARD_SIZE = 5
DEFAULT_PLAYERS = (Player(label="x", color="blue"),
                   Player(label="O", color="green"))

class TicTacToeGame:
    def __init__(self, players:DEFAULT_PLAYERS, board_size = BOARD_SIZE):
        self._players = cycle(players)  #cycles over player tuple
        self.board_size = board_size    
        self.current_player = next(self.__players)
        self.winner_combo=[]        #combo that defines winner
        self._current_moves = []    #list of player moves
        self._has_winner = False    #if win
        self._winning.combos = []   #list with combos that make a win
        self._setup_board()
    
    def _setup_board(self):
        self._current_moves = [[Move(row, col) for col in range(self.board_size)]
                               for row in range(self.board_size)]   #initial list of player moves
        self._winning_combos = self._get_winning_combos()
    
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]



class TicTacToeBoard(tk.Tk):                #class inherits from Tk
    def __init__(self):
        super().__init__()                  #initialize parent class
        self.title("Infinite Tic-Tac-Toe")  #title bar
        self._cells = {}                     #dictionary for row and column of cells
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)       #frame object holds display, main window is parent
        display_frame.pack(fill=tk.X)               #fill's screen with game board
        self.display = tk.Label(master=display_frame, 
                                text="Ready?", 
                                font=font.Font(size=28, weight="bold"))
        self.display.pack()

    def _create_board_grid(self): 
        grid_frame = tk.Frame(master = self)    #create frame for board frame
        grid_frame.pack()                       #puts it on main window
        for row in range(BOARD_SIZE):
            self.rowconfigure(row, weight=1, minsize=50)        #cell weidght and height
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(BOARD_SIZE):
                button = tk.Button(master=grid_frame, text="", 
                                font = font.Font(size=36, weight="bold"),
                                fg="black", width=3, height=2,
                                highlightbackground="lightblue")
                self._cells[button] = (row,col)             #adds every new button to the dictionary
                button.grid(row=row, column=col,padx=5,pady=5,sticky="nsew")

#initializes game
def main():
    board = TicTacToeBoard()
    board.mainloop()

if __name__ == "__main__":
    main()
