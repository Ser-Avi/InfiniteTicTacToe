"""
Created by Avi Serebrenik
An adjustable tic-tac-toe game built with Python and Tkinter.
The base tic-tac-toe game was found in the following guide: https://realpython.com/tic-tac-toe-python/
"""

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple):   #player class
    label: str  #store x or o
    color:str   #color for player indentification
    player_name: str    #name of player for turn toggle

class Move(NamedTuple):     #class for each move
    row:int     #coordinates of move
    col:int
    label:str = ""  #whether move is legal

#global variables for default setting adjusting
BOARD_SIZE = 2
WIN_SIZE = 2
MAX_WIN = 8
MAX_SIZE = 15
BIG_BOARD = False
DEFAULT_PLAYERS = (Player(label="X", color="blue", player_name = "X"),
                   Player(label="O", color="green", player_name="O"))


class StartScreen(tk.Tk):
    """Creates the start screen before the game"""
    def __init__(self, board_size = BOARD_SIZE, win_size = WIN_SIZE, default_players = DEFAULT_PLAYERS, big_board = BIG_BOARD):
        super().__init__()                  #initialize parent class
        self.board_size = board_size
        self.win_size = win_size
        self.players = default_players
        self.big_board = big_board
        self.title("Mega Tic-Tac-Toe")      #title bar
        self._create_display()
        self._create_screen()
        self._set_name()

    def _create_display(self):
        """Creates the base display frame"""
        display_frame = tk.Frame(master=self)       #frame object holds display, main window is parent
        display_frame.pack(fill=tk.X)               
        self.display = tk.Label(master=display_frame,   #creates display title
                                text="Mega Tic Tac Toe", 
                                font=font.Font(size=28, weight="bold"),
                                padx=100)
        self.display.pack()
    
    def _create_screen(self):
        """Creates the sliders and button in the start screen"""
        screen_frame = tk.Frame(master = self)    #create frame for board frame
        screen_frame.pack()
        size_scale = tk.Scale(master = screen_frame,    #scale for size adjustment
                              orient = "horizontal",
                              from_ = 2,
                              to=MAX_SIZE,
                              command = self.board_adjust)
        win_scale = tk.Scale(master = screen_frame,     #scale for win adjustment
                              orient = "horizontal",
                              from_ = 2,
                              to=MAX_WIN,
                              command = self.win_adjust)
        size_name = tk.Label(master = screen_frame,
                              text = "Board Size:")
        win_name = tk.Label(master = screen_frame,
                              text = "Win Size:")
        size_name.grid(row = 1, column = 0, pady = 15)
        size_scale.grid(row = 1, column = 2, pady = 15)
        win_name.grid(row = 2, column = 0, padx = 10)
        win_scale.grid(row = 2, column = 2)
    
    def _set_name(self):
        """Sets name of players based on input and has start button"""
        name_frame = tk.Frame(master = self)    #create frame for board frame
        name_frame.pack()
        zero_label = tk.Label(master = name_frame, text = "Player O Name:")
        x_label = tk.Label (master = name_frame, text = "Player X Name:")
        zero_label.grid(row = 0, column = 0)
        x_label.grid(row = 1, column = 0)
        name_zero = tk.Entry(master = name_frame)
        name_zero.grid(row = 0, column = 1)
        name_x = tk.Entry(master = name_frame)
        name_x.grid(row = 1, column = 1)
        start_button = tk.Button(master = name_frame, #button to start game
                                 text = "Start",
                                 command = lambda:[self.name_adjust(name_zero.get(),name_x.get()),
                                                   self.destroy(),self.start_game()])
        start_button.grid(row = 4, column = 1, pady = 15)
    
    def start_game(self):
        game = TicTacToeGame(board_size = self.board_size,
                         win_size = self.win_size,
                         players = self.players)
        board = TicTacToeBoard(game, big_board = self.big_board)
        board.mainloop()
    
    def board_adjust(self,i):
        """Adjusts board size"""
        self.board_size = int(i)
        if int(i)>10:
            self.big_board = True
        else:
            self.big_board = False
    
    def win_adjust(self, i):
        """Adjusts win size"""
        self.win_size = int(i)
    
    def name_adjust(self, zero, x):
        """Adjusts player names"""
        if x =="":
            x = "X"
        if zero == "":
            zero = "O"
        player_zero = self.players[1]
        player_x = self.players[0]
        self.players = (Player(label = player_x.label, color = player_x.color, player_name = x ),
                        Player(label = player_zero.label, color = player_zero.color, player_name = zero))


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size = BOARD_SIZE, win_size = WIN_SIZE):
        self._players = cycle(players)  #cycles over player tuple
        self.board_size = board_size
        self.win_size = win_size    
        self.current_player = next(self._players)
        self.winner_combo=[]        #combo that defines winner
        self._current_moves = []    #list of player moves
        self._has_winner = False    #if win
        self._winning_combos = []   #list with combos that make a win
        self._setup_board()
    
    def _setup_board(self):
        self._current_moves = [[Move(row, col) for col in range(self.board_size)]
                               for row in range(self.board_size)]   #initial list of player moves
        self._winning_combos = self._get_winning_combos()
    
    def _get_winning_combos(self):
        """Returns an array of all possible winning combinations"""
        rows = []
        columns = []
        first_diagonal = [] #Diagonals with negative slope
        second_diagonal = [] #Diagonals with positive slope
        for i in range(self.board_size):        #rows
            for j in range(self.board_size-self.win_size+1):    #columns
                rows.append([])
                columns.append([])
                if i<self.board_size-self.win_size+1:
                    first_diagonal.append([])
                #second_diagonal.append([])
                for k in range(self.win_size):  #length of each win
                    rows[i*(self.board_size-self.win_size+1)+j].append((i, j+k))
                    columns[i*(self.board_size-self.win_size+1)+j].append((j+k, i))
                    if i<self.board_size-self.win_size+1:
                        first_diagonal[i*(self.board_size-self.win_size+1)+j].append((i+k,j+k))
        #second loop for second diagonal->easier to set up this way
        for i in range(self.win_size-1, self.board_size):       #rows
            for j in range(self.board_size-self.win_size+1):    #columns
                second_diagonal.append([])
                for k in range(self.win_size):                  #length of each win
                    second_diagonal[(i-self.win_size+1)*(self.board_size-self.win_size+1)+j].append((i-k,j+k))
        return rows + columns + first_diagonal + second_diagonal

    def is_valid_move(self, move):
        """Returns True if move is valid->no winner yet and square is empty"""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self, move):
        """Makes move and checks if current move is win"""
        row, col = move.row, move.col
        self._current_moves[row][col] = move    #input assigned to [row][col] in current moves
        for combo in self._winning_combos:      #loop over winning combos
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results)==1) and (""not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """True if game has winner"""
        return self._has_winner
    
    def is_tied(self):
        """Checks if game is tied"""
        no_winner = not self._has_winner    #no winner yet
        #check if all cells have a string->a move
        played_moves = (move.label for row in self._current_moves for move in row)
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        """Cicles between players"""
        self.current_player = next(self._players)
    
    def reset_game(self):
        """Starts a new game"""
        for row, row_content in enumerate(self._current_moves):     #resets all moves to empty
            for col,_ in enumerate(row_content):
                row_content[col]=Move(row, col)
        self._has_winner = False    #resets winner
        self.winner_combo = []      #resets winning move


class TicTacToeBoard(tk.Tk):                #class inherits from Tk
    def __init__(self, game, big_board = BIG_BOARD):
        super().__init__()                  #initialize parent class
        self.title("Mega Tic-Tac-Toe")      #title bar
        self._cells = {}                     #dictionary for row and column of cells
        self._game = game
        self.big_board = big_board
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        """Creates the display window and ready text"""
        display_frame = tk.Frame(master=self)       #frame object holds display, main window is parent
        display_frame.pack(fill=tk.X)               #fill's screen with game board
        if self.big_board:
            self.display = tk.Label(master=display_frame, 
                                text=f"Ready? {self._game.current_player.player_name} starts", 
                                font=font.Font(size=16, weight="bold"))
        else:
            self.display = tk.Label(master=display_frame, 
                                    text=f"Ready? {self._game.current_player.player_name} starts", 
                                    font=font.Font(size=28, weight="bold"))
        self.display.pack()

    def _create_board_grid(self):
        """Creates the button grid for the game board""" 
        grid_frame = tk.Frame(master = self)    #create frame for board frame
        grid_frame.pack()                       #puts it on main window
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)        #cell widght and height
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                if self.big_board:
                    button = tk.Button(master = grid_frame, text="",
                                        font = font.Font(size=12, weight="bold"),
                                        fg="black", width=3, height=2,
                                        highlightbackground="lightblue")
                else:
                    button = tk.Button(master=grid_frame, text="", 
                                font = font.Font(size=24, weight="bold"),
                                fg="black", width=3, height=2,
                                highlightbackground="lightblue")
                self._cells[button] = (row,col)             #adds every new button to the dictionary
                button.bind("<ButtonPress-1>", self.play)    #play gets run when button is pressed
                button.grid(row=row, column=col,padx=5,pady=5,sticky="nsew")
    
    def play(self, event):
        """Handles player moves""" 
        clicked_btn = event.widget              #retrieves button that triggered event
        row, col = self._cells[clicked_btn]     #cell's coordinates
        move = Move(row, col, self._game.current_player.label)
        self.play_again = tk.Button(text = "Play Again?", command = self.reset_board)
        self.change_settings = tk.Button(text = "Change Settings", command = lambda:[self.destroy(),main()])
        if self._game.is_valid_move(move):      #if move is valid
            self._update_button(clicked_btn)    #set button to player
            self._game.process_move(move)       #process move
            if self._game.is_tied():            #check if game is tied
                self._update_display(msg = "Tied!", color = "green")
                self.play_again.pack()
                self.change_settings.pack()
            elif self._game.has_winner():       #check if game is won
                self._highlight_cells()         #highlight winning cells
                msg = f'Player "{self._game.current_player.player_name}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)    #update display to winner message
                self.play_again.pack()
                self.change_settings.pack()
            else:
                self._game.toggle_player()      #no winner or tie->continue with next player
                msg = f"{self._game.current_player.player_name}'s turn"
                self._update_display(msg)
    
    def _update_button(self, clicked_btn):
        """Updates button to current player's"""
        clicked_btn.config(text = self._game.current_player.label)
        clicked_btn.config(fg = self._game.current_player.color)
    
    def _update_display(self, msg, color="black"):
        """Updates game display"""
        self.display["text"] = msg
        self.display["fg"] = color
    
    def _highlight_cells(self):
        """Highlighting cells for a win"""
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground = "red")
    
    def reset_board(self):
        """Resets the game board"""
        self._game.reset_game()         #calls upon reset_game method
        self._update_display(msg = f"Ready? {self._game.current_player.player_name} starts")    #reset board display
        self.play_again.pack_forget()
        self.change_settings.pack_forget()
        for button in self._cells.keys():       #loops over each button to reset them
            button.config(highlightbackground = "lightblue")
            button.config(text = "")
            button.config(fg = "black")


#initializes game
def main():
    start = StartScreen()
    start.mainloop()

if __name__ == "__main__":
    main()