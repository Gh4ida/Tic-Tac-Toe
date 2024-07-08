from flask import Flask, request, jsonify
import threading
import time
import random
import string

app = Flask(__name__)

# Dictionary to store game states for different rooms
rooms = {}

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def reset_game_state(room_code):
    time.sleep(3)
    rooms[room_code] = {
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "player": "X",
        "win": 0,
        "message": "",
        "players": {"X": None, "O": None}
    }

@app.route('/create_room', methods=['POST'])
def create_room():
    room_code = generate_room_code()
    rooms[room_code] = {
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "player": "X",
        "win": 0,
        "message": "",
        "players": {"X": "playerX", "O": None}  # Dummy player name
    }
    return jsonify({"room_code": room_code})

@app.route('/join_room', methods=['POST'])
def join_room():
    room_code = request.json['room_code']
    if room_code in rooms and rooms[room_code]['players']['O'] is None:
        rooms[room_code]['players']['O'] = "playerO"  # Dummy player name
        return jsonify({"room_code": room_code})
    return jsonify({"error": "Room not found or already full"}), 400

@app.route('/get_state/<room_code>', methods=['GET'])
def get_state(room_code):
    if room_code in rooms:
        return jsonify(rooms[room_code])
    return jsonify({"error": "Room not found"}), 404

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    room_code = data['room_code']
    row, col, player = data['row'], data['col'], data['player']
    if room_code in rooms:
        game_state = rooms[room_code]
        if game_state['board'][row][col] == "" and game_state['win'] == 0:
            game_state['board'][row][col] = player
            if check_winner(game_state['board']):
                game_state['win'] = 1
                game_state['message'] = f"{player} is the winner"
                threading.Thread(target=reset_game_state, args=(room_code,)).start()
            elif check_tie(game_state['board']):
                game_state['win'] = 1
                game_state['message'] = "It is a tie!"
                threading.Thread(target=reset_game_state, args=(room_code,)).start()
            else:
                game_state['player'] = "O" if player == "X" else "X"
            return jsonify(game_state)
    return jsonify({"error": "Invalid move"}), 400

def check_winner(board):
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

def check_tie(board):
    for row in board:
        if "" in row:
            return False
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)