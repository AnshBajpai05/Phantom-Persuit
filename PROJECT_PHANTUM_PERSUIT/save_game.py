# save_game.py
import json

# File to store game history
GAME_HISTORY_FILE = "games.json"

def save_game(username, moves, winner):
    # Load existing data
    try:
        with open(GAME_HISTORY_FILE, "r") as file:
            games = json.load(file)
    except FileNotFoundError:
        games = {}

    # Append the game history under the username
    if username not in games:
        games[username] = []
    games[username].append({
        "moves": moves,
        "winner": winner
    })

    # Save back to the file
    with open(GAME_HISTORY_FILE, "w") as file:
        json.dump(games, file, indent=4)

    print(f"Game saved for user '{username}'.")

# Example usage
if __name__ == "__main__":
    save_game("player1", ["X at (0, 0)", "O at (1, 1)", "X at (0, 1)", "O at (2, 2)", "X at (0, 2)"], "X")
