from tkinter import *

window = Tk()
window.title('TicTacToe')
window.geometry("400x400")
window.resizable(False, False)

# Function to create a grid line 
def create_grid_line(x0, y0, x1, y1, color="black", width=2):
    canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

# Create the canvas
canvas = Canvas(window, width=400, height=400, bg="white")
canvas.pack()
# Draw the grid lines
grid_width = 400
grid_spacing = grid_width // 3  # Divide width into 3 equal sections
board = [["", "", ""], ["", "", ""], ["", "", ""]] 
player = "X"
win = 0

def create_board():
    create_grid_line(0, grid_spacing, grid_width, grid_spacing)
    create_grid_line(0, grid_spacing * 2, grid_width, grid_spacing * 2)
    create_grid_line(grid_spacing, 0, grid_spacing, grid_width)
    create_grid_line(grid_spacing * 2, 0, grid_spacing * 2, grid_width)

create_board()
# Function to place X or O on the board
def place_symbol(x, y):
    global win
    global player
    cell_width = grid_spacing
    col = x // cell_width
    row = y // cell_width

    if win == 1:
        return reset_board()

    if board[row][col] == "":
        cell_center_x = (col * cell_width) + (cell_width // 2)
        cell_center_y = (row * cell_width) + (cell_width // 2)

        if player == "X":
            canvas.create_text(cell_center_x, cell_center_y, text="X", font=("Arial", 45), fill="blue")
            board[row][col] = "X"
            if winner():
                win = 1
                print(f"{player} is the winner")
            elif draw():
                win = 1
                print("No one wins!")
            player = "O"
        else:
            canvas.create_text(cell_center_x, cell_center_y, text="O", font=("Arial", 45), fill="red")
            board[row][col] = "O"
            if winner():
                win = 1
                print(f"{player} is the winner")
            elif draw():
                win = 1
                print("No one wins!")
            player = "X"

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

def draw():
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
    create_board()

# Function to handle the click event on the canvas
def click_handler(event):
    place_symbol(event.x, event.y)

# Bind the click event to the canvas
canvas.bind("<Button-1>", click_handler)

window.mainloop()
