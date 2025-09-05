import socket
import threading
import time
#N
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.131.2", 5555))
    server.listen(3)  # Allow three players to connect
    print("Server started. Waiting for players...")

    connections = []
    player_names = []
    for i in range(3):
        conn, addr = server.accept()
        print(f"Player {i+1} connected: {addr}")
        conn.sendall("Enter your name: ".encode())
        name = conn.recv(1024).decode().strip().split()[0]  # Take the first word of the name
        player_names.append(name)
        connections.append(conn)
        conn.sendall(f"Welcome, {name}! Waiting for other players...\n".encode())

    # Game settings
    grid_size = 16
    player_positions = [[15, 15], [15, 0], [0, 15]]  # Initial positions for three players
    ghost_position = [1, 1]
    game_over = False
    start_time = time.time()

    # Generate the game grid
    #N
    def generate_grid():
        grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
        for i, pos in enumerate(player_positions):
            grid[pos[0]][pos[1]] = player_names[i][:2].upper()  # Use the first two letters of the name
        grid[ghost_position[0]][ghost_position[1]] = "G"
        return grid

    # Send the grid and timer to all players
    # A
    def send_grid_and_timer():
        grid = generate_grid()
        grid_str = "\n".join([" ".join(row) for row in grid]) + "\n"
        elapsed_time = time.time() - start_time
        time_left = 25 - int(elapsed_time)  # 25-second timer
        if time_left > 0:
            timer_str = f"\nTime left: {time_left} seconds\n"
        else:
            timer_str = "\nTime's up!\n"
        
        message = timer_str + grid_str
        for conn in connections:
            conn.sendall(message.encode())

    # Ghost movement logic (AI targets nearest player)
    #A
    def move_ghost():
        distances = [abs(ghost_position[0] - p[0]) + abs(ghost_position[1] - p[1]) for p in player_positions]
        target = player_positions[distances.index(min(distances))]
        
        if ghost_position[0] < target[0]:
            ghost_position[0] += 1
        elif ghost_position[0] > target[0]:
            ghost_position[0] -= 1
        if ghost_position[1] < target[1]:
            ghost_position[1] += 1
        elif ghost_position[1] > target[1]:
            ghost_position[1] -= 1

    # Game loop
    #A
    def game_loop():
        nonlocal game_over
        while not game_over:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 25:
                message = "You survived 25 seconds! You win!\n"
                for conn in connections:
                    conn.sendall(message.encode())
                game_over = True
                break
            
            for i, pos in enumerate(player_positions):
                if pos == ghost_position:
                    message = f"{player_names[i]} was caught by the ghost! Game over.\n"
                    for conn in connections:
                        conn.sendall(message.encode())
                    game_over = True
                    break

            send_grid_and_timer()
            time.sleep(0.5)

    # Handle player input
    #A
    def handle_player_input(player_id, conn):
        nonlocal game_over
        while not game_over:
            try:
                move = conn.recv(1024).decode().strip().upper()
                if move == "W" and player_positions[player_id][0] > 0:
                    player_positions[player_id][0] -= 1
                elif move == "S" and player_positions[player_id][0] < grid_size - 1:
                    player_positions[player_id][0] += 1
                elif move == "A" and player_positions[player_id][1] > 0:
                    player_positions[player_id][1] -= 1
                elif move == "D" and player_positions[player_id][1] < grid_size - 1:
                    player_positions[player_id][1] += 1
                elif move == "EXIT":
                    game_over = True
                    break
            except:
                break

    # Start threads
    threading.Thread(target=game_loop, daemon=True).start()
    for i, conn in enumerate(connections):
        threading.Thread(target=handle_player_input, args=(i, conn), daemon=True).start()

    while not game_over:
        move_ghost()
        time.sleep(1)

    for conn in connections:
        conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
