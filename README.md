# Phantom-Persuit
Phantom Pursuit is a Python survival game where players evade a ghost on a dynamic graph. The ghost uses AI pathfinding (BFS, Dijkstra, A*), with difficulty-based behavior. Features include a sanity system, power-ups, MySQL stat tracking, sound effects, visual gameplay, and replayable history.


🎮 Features

Dynamic Graph Map:

Built using NetworkX with random geometric graphs.

Weighted edges for Hard mode with real-time visualization via Matplotlib.

Game Modes & Difficulty:

Player vs AI (Ghost with BFS, Dijkstra, or A* pathfinding depending on difficulty).

Three difficulty levels: Easy, Medium, Hard.

Ghost Mechanics:

Ghost alternates between wandering and hunting mode.

Different movement strategies per difficulty.

Sanity system where proximity to the ghost drains your sanity faster.

Power-Ups & Items:

Booster Tablets: Restore sanity.

Hearts of the Dead: Allow player respawn after being caught.

Persistence & Stats:

Integrated with MySQL database (user_stats table).

Tracks games played, best score, total score, and Hearts collected.

In-game store to exchange score points for Hearts of the Dead.

Sound & Visual Effects:

Pygame mixer for creepy sound effects.

Loading screen with Tkinter + PIL.

Real-time graph visualization of player and ghost positions.

Replay Feature:

Review your move history after game over.

🛠️ Tech Stack

Python (Core logic)

NetworkX (Graph generation & pathfinding)

Matplotlib (Game visualization)

Tkinter + PIL (Loading screen UI)

Pygame (Sound effects)

MySQL (Player stats persistence)
