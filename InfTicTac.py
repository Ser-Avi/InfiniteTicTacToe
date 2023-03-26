"""
Created by Avi Serebrenik
An infinite tic-tac-toe game built with Python and Tkinter.
The base tic-tac-toe game was found in the following guide: https://realpython.com/tic-tac-toe-python/
"""

import tkinter as tk
from tkinter import font

gameSize = 3

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
        for row in range(gameSize):
            self.rowconfigure(row, weight=1, minsize=50)        #cell weidght and height
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(gameSize):
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
