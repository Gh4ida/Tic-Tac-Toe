import asyncio
import aiohttp
from tkinter import *
import threading

SERVER_URL = 'http://x.x.x.x:5000'  # Change this to your server's URL

window = Tk()
window.title('TicTacToe')
window.geometry("400x550")
window.resizable(False, False)

# Create a label for displaying game result
result_label = Label(window, text="", font=("Arial", 16))
result_label.pack()

# Create the canvas
canvas = Canvas(window, width=400, height=400, bg="white")
canvas.pack()

# Create a label for room code entry
room_label = Label(window, text="Room Code:", font=("Arial", 12))
room_label.pack()

room_code_entry = Entry(window)
room_code_entry.pack()

# Create a frame to hold the create and join buttons
button_frame = Frame(window)
button_frame.pack(pady=10)

# Create buttons to create or join a room
create_button = Button(button_frame, text="Create Room", command=lambda: asyncio.run(create_or_join_room("create")))
create_button.pack(side=LEFT, padx=5)

join_button = Button(button_frame, text="Join Room", command=lambda: asyncio.run(create_or_join_room("join")))
join_button.pack(side=LEFT, padx=5)

# Label to display the room code after creation
room_code_label = Label(window, text="", font=("Arial", 16))

# Draw the grid lines
grid_width = 400
cell = grid_width // 3  # Divide width into 3 equal sections

def create_grid_line(x0, y0, x1, y1, color="black", width=2):
    canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

def create_board():
    create_grid_line(0, cell, grid_width, cell)
    create_grid_line(0, cell * 2, grid_width, cell * 2)
    create_grid_line(cell, 0, cell, grid_width)
    create_grid_line(cell * 2, 0, cell * 2, grid_width)

create_board()

room_code = None
player = None

async def create_or_join_room(action):
    global room_code, player
    async with aiohttp.ClientSession() as session:
        if action == "create":
            async with session.post(f'{SERVER_URL}/create_room') as response:
                if response.status == 200:
                    data = await response.json()
                    room_code = data['room_code']
                    player = "X"
                    result_label.config(text=f"Room created! You are player X.")
                    room_code_label.config(text=f"Room Code: {room_code}")
                    room_code_label.pack()
                    button_frame.pack_forget()
                    room_code_entry.pack_forget()
                    room_label.pack_forget()
        elif action == "join":
            room_code = room_code_entry.get()
            async with session.post(f'{SERVER_URL}/join_room', json={'room_code': room_code}) as response:
                if response.status == 200:
                    player = "O"
                    result_label.config(text=f"Joined room {room_code}. You are player O.")
                    button_frame.pack_forget()
                    room_code_entry.pack_forget()
                    room_label.pack_forget()
                else:
                    result_label.config(text="Error joining room. Make sure the room code is correct and the room is not full.")

async def get_game_state():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{SERVER_URL}/get_state/{room_code}') as response:
            if response.status == 200:
                return await response.json()
    return None

async def update_board(state):
    canvas.delete("all")
    create_board()
    board = state['board']
    for row in range(3):
        for col in range(3):
            if board[row][col] != "":
                cell_center_x = (col * cell) + (cell // 2)
                cell_center_y = (row * cell) + (cell // 2)
                canvas.create_text(cell_center_x, cell_center_y, text=board[row][col], font=("Arial", 45), fill="blue" if board[row][col] == "X" else "red")
    result_label.config(text=state['message'] if state['win'] == 1 else f"{state['player']}'s turn")

async def place_symbol(x, y):
    if room_code is None:
        result_label.config(text="Please create or join a room first.")
        return
    state = await get_game_state()
    if state['win'] == 1:
        return
    cell_width = cell
    col = x // cell_width
    row = y // cell_width
    if state['board'][row][col] == "" and state['player'] == player:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{SERVER_URL}/make_move', json={'room_code': room_code, 'row': row, 'col': col, 'player': player}) as response:
                if response.status == 200:
                    state = await response.json()
                    await update_board(state)

async def reset_board():
    state = await get_game_state()
    if state:
        await update_board(state)

def click_handler(event):
    asyncio.run(place_symbol(event.x, event.y))

async def auto_refresh():
    while True:
        if room_code is not None:
            await reset_board()
        await asyncio.sleep(2)

canvas.bind("<Button-1>", click_handler)

# Create a thread to run the async event loop
def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(auto_refresh())

new_loop = asyncio.new_event_loop()
threading.Thread(target=start_async_loop, args=(new_loop,), daemon=True).start()

window.mainloop()
