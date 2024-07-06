from tkinter import *

# Function to create a grid line on the canvas
def create_grid_line(x0, y0, x1, y1, color="black", width=2):
    canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

# Function to draw X
def draw_x(x, y):
    offset = 20
    canvas.create_line(x - offset, y - offset, x + offset, y + offset, fill="blue", width=2)
    canvas.create_line(x - offset, y + offset, x + offset, y - offset, fill="blue", width=2)

# Function to draw O
def draw_o(x, y):
    offset = 20
    canvas.create_oval(x - offset, y - offset, x + offset, y + offset, outline="red", width=2)

# Create the main window
window = Tk()
window.title('TicTacToe')
window.geometry("400x400")
window.resizable(False, False)

# Create the canvas
canvas = Canvas(window, width=400, height=400, bg="white")
canvas.pack()

# Draw the grid lines
grid_width = 400
grid_spacing = grid_width // 3  # Divide width into 3 equal sections

# Horizontal lines
create_grid_line(0, grid_spacing, grid_width, grid_spacing)
create_grid_line(0, grid_spacing * 2, grid_width, grid_spacing * 2)

# Vertical lines
create_grid_line(grid_spacing, 0, grid_spacing, grid_width)
create_grid_line(grid_spacing * 2, 0, grid_spacing * 2, grid_width)

# Drawing X and O shapes
draw_x(grid_spacing // 2, grid_spacing // 2) # Top left
draw_o(grid_spacing * 3 // 2, grid_spacing * 3 // 2) # Center

window.mainloop()
