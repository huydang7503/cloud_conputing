from flask import Flask, render_template, request

app = Flask(__name__)

board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

turn = "X"
game_end = False
mode = "multiPlayer"

def check_for_win(player):
    # Kiểm tra các hàng
    for i in range(0, 3):
        if board[1 + i * 3] == board[2 + i * 3] == board[3 + i * 3] == player:
            return True

    # Kiểm tra các cột
    for i in range(0, 3):
        if board[1 + i] == board[4 + i] == board[7 + i] == player:
            return True

    # Kiểm tra đường chéo
    if board[1] == board[5] == board[9] == player:
        return True
    if board[3] == board[5] == board[7] == player:
        return True

    return False

def check_for_draw():
    for i in board.keys():
        if board[i] == " ":
            return False
    return True

def play_computer():
    best_score = -10
    best_move = 0

    for key in board.keys():
        if board[key] == " ":
            board[key] = "O"
            score = minimax(board, False)  # Sử dụng thuật toán minimax
            board[key] = " "
            if score > best_score:
                best_score = score
                best_move = key

    board[best_move] = "O"

def minimax(board, is_maximizing):
    if check_for_win("O"):
        return 1

    if check_for_win("X"):
        return -1

    if check_for_draw():
        return 0

    if is_maximizing:
        best_score = -1
        for key in board.keys():
            if board[key] == " ":
                board[key] = "O"
                score = minimax(board, False)
                board[key] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1
        for key in board.keys():
            if board[key] == " ":
                board[key] = "X"
                score = minimax(board, True)
                board[key] = " "
                best_score = min(score, best_score)
        return best_score

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    global turn, game_end, mode
    cell = int(request.form["cell"])

    if board[cell] == " ":
        board[cell] = turn

        if check_for_win(turn):
            result = f"{turn} wins the game!"
            game_end = True
        elif check_for_draw():
            result = "Game Draw!"
            game_end = True
        else:
            result = None

        if mode == "multiPlayer":
            turn = "O" if turn == "X" else "X"
        else:
            play_computer()
            if check_for_win("O"):
                result = "Computer wins the game!"
                game_end = True
            elif check_for_draw():
                result = "Game Draw!"
                game_end = True

            turn = "X"

        return {"result": result, "board": board, "game_end": game_end}

@app.route("/restart", methods=["POST"])
def restart():
    global board, turn, game_end
    board = {1: " ", 2: " ", 3: " ",
             4: " ", 5: " ", 6: " ",
             7: " ", 8: " ", 9: " "}
    turn = "X"
    game_end = False
    return {"board": board, "turn": turn, "game_end": game_end}

@app.route("/mode", methods=["POST"])
def change_mode():
    global mode
    mode = request.form["mode"]
    return {"mode": mode}

if __name__ == "__main__":
    app.run(debug=True)
