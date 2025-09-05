# replay_game.py
import tkinter as tk
import json
import time

GAME_HISTORY_FILE = "games.json"

def replay_game(username, game_index):
    try:
        with open(GAME_HISTORY_FILE, "r") as file:
            games = json.load(file)
    except FileNotFoundError:
        print("No game history found.")
        return

    if username not in games or game_index >= len(games[username]):
        print("Invalid username or game index.")
        return

    game = games[username][game_index]
    moves = game["moves"]

    # Initialize Tkinter
    root = tk.Tk()
    root.title(f"Replay for {username} - Game {game_index + 1}")

    # Create the board
    buttons = [[None for _ in range(3)] for _ in range(3)]

    def update_board(x, y, symbol):
        buttons[x][y].config(text=symbol, state="disabled")

    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(root, text="", font=("Arial", 24), width=5, height=2)
            buttons[i][j].grid(row=i, column=j)

    # Replay moves
    for move in moves:
        parts = move.split(" ")
        symbol = parts[0]
        x, y = map(int, parts[-1][1:-1].split(","))
        root.update()
        time.sleep(1)  # Wait for 1 second between moves
        update_board(x, y, symbol)

    # Show winner or draw
    result = tk.Label(root, text=f"Winner: {game['winner']}" if game["winner"] else "It's a draw!", font=("Arial", 16))
    result.grid(row=3, column=0, columnspan=3)

    root.mainloop()

# Example usage
if __name__ == "__main__":
    replay_game("player1", 0)
