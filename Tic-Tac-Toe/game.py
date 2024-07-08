from tkinter import *

# Create a window
window = Tk()
window.title('TicTacToe')
window.geometry("400x430")
window.resizable(False, False)

# Create a label bar for displaying the game's result
result_label = Label(window, text="", font=("Arial", 16))
result_label.pack()

# Create the canva
canvas = Canvas(window, width=400, height=400, bg="white")
canvas.pack()

# Draw the grid lines
grid_width = 400
cell = grid_width // 3  # Divide width into 3 equal sections
board = [["", "", ""], ["", "", ""], ["", "", ""]] 
player = "X"
result_label.config(text=f"{player}'s turn")
win = 0

def create_grid_line(x0, y0, x1, y1, color="black", width=2):
    canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

def create_board():
    create_grid_line(0, cell, grid_width, cell)
    create_grid_line(0, cell * 2, grid_width, cell * 2)
    create_grid_line(cell, 0, cell, grid_width)
    create_grid_line(cell * 2, 0, cell * 2, grid_width)

create_board()
# Function to place X or O on the board
def place_symbol(x, y):
    global win, player
    cell_width = cell
    col = x // cell_width
    row = y // cell_width

    if win == 1:
        reset_board()
        return

    if board[row][col] == "":
        cell_center_x = (col * cell_width) + (cell_width // 2)
        cell_center_y = (row * cell_width) + (cell_width // 2)

        if player == "X":
            result_label.config(text=f"{player}'s turn")

            canvas.create_text(cell_center_x, cell_center_y, text="X", font=("Arial", 45), fill="blue")
            board[row][col] = "X"
            if winner():
                win = 1
                result_label.config(text=f"{player} is the winner")
                return
            elif tie():
                win = 1
                result_label.config(text="It is a tie!")
                return
            player = "O"
            result_label.config(text=f"{player}'s turn")

        else:
            result_label.config(text=f"{player}'s turn")

            canvas.create_text(cell_center_x, cell_center_y, text="O", font=("Arial", 45), fill="red")

            board[row][col] = "O"
            if winner():
                win = 1
                result_label.config(text=f"{player} is the winner")
                return
            elif tie():
                win = 1
                result_label.config(text="It is a tie!")
                return
            player = "X"
        
            result_label.config(text=f"{player}'s turn")

def winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return True
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True
    elif board[0][2] == board[1][1] == board[2][0] != "":
        return True
    return False

def tie():
    for row in board:
        if "" in row:
            return False
    return True

def reset_board():
    global board, player, win
    canvas.delete("all") 
    board = [["", "", ""], ["", "", ""], ["", "", ""]] 
    player = "X"
    win = 0
    result_label.config(text=f"{player}'s turn")
    create_board()

# Function to handle the click event on the canvas
def click_handler(event):
    place_symbol(event.x, event.y)

# Bind the click event to the canvas
canvas.bind("<Button-1>", click_handler)

window.mainloop()
