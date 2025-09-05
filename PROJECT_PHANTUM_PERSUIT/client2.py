# import socket
# import json
# import keyboard
# import os
# import threading
# import time

# class GameClient:
#     def __init__(self, host='192.168.50.6', port=5555):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.connect((host, port))
#         self.player_type = self.client.recv(1024).decode()
#         print(f"You are the {self.player_type}!")
#         self.running = True

#     def receive_state(self):
#         while self.running:
#             try:
#                 data = self.client.recv(1024).decode()
#                 state = json.loads(data)
#                 self.display_game(state)
#             except:
#                 break

#     def display_game(self, state):
#         os.system('cls' if os.name == 'nt' else 'clear')
#         positions = state['positions']
        
#         print("Ghost Game - You are the", self.player_type)
#         print("Use arrow keys to move")
#         print("Press 'q' to quit")
#         print("-" * 20)
        
#         for y in range(10):
#             for x in range(10):
#                 ghost_here = (x == positions['ghost']['x'] and y == positions['ghost']['y'])
#                 player_here = (x == positions['player']['x'] and y == positions['player']['y'])
                
#                 if ghost_here and player_here:
#                     print('X', end=' ')
#                 elif ghost_here:
#                     print('G', end=' ')
#                 elif player_here:
#                     print('P', end=' ')
#                 else:
#                     print('.', end=' ')
#             print()
        
#         if state['caught']:
#             print("\nGame Over! Ghost caught the player!")

#     def handle_input(self):
#         while self.running:
#             try:
#                 # Check for movement keys
#                 if keyboard.is_pressed('up'):
#                     self.client.send('up'.encode())
#                     time.sleep(0.1)  # Add small delay to prevent too rapid movement
#                 elif keyboard.is_pressed('down'):
#                     self.client.send('down'.encode())
#                     time.sleep(0.1)
#                 elif keyboard.is_pressed('left'):
#                     self.client.send('left'.encode())
#                     time.sleep(0.1)
#                 elif keyboard.is_pressed('right'):
#                     self.client.send('right'.encode())
#                     time.sleep(0.1)
#                 elif keyboard.is_pressed('q'):  # Add quit option
#                     self.running = False
#                     break
                
#                 time.sleep(0.05)  # Small sleep to prevent high CPU usage
#             except:
#                 self.running = False
#                 break

#     def start(self):
#         # Start receive thread
#         receive_thread = threading.Thread(target=self.receive_state)
#         receive_thread.daemon = True
#         receive_thread.start()
        
#         # Start input thread
#         input_thread = threading.Thread(target=self.handle_input)
#         input_thread.daemon = True
#         input_thread.start()
        
#         # Keep main thread alive
#         try:
#             while self.running:
#                 time.sleep(0.1)
#         except KeyboardInterrupt:
#             self.running = False
        
#         self.client.close()

# if __name__ == "__main__":
#     client = GameClient()
#     client.start()

import socket
import json
import keyboard
import os
import threading
import time

class GameClient:
    def __init__(self, host='192.168.50.6', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.player_type = self.client.recv(1024).decode()
        print(f"You are the {self.player_type}!")
        self.running = True
        self.game_over = False

    def receive_state(self):
        while self.running:
            try:
                data = self.client.recv(1024).decode()
                state = json.loads(data)
                self.game_over = state['game_over']
                self.display_game(state)
                
                if self.game_over:
                    self.running = False
            except:
                break

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def display_game(self, state):
        os.system('cls' if os.name == 'nt' else 'clear')
        positions = state['positions']
        
        print(f"Ghost Game - You are the {self.player_type}")
        print(f"Time remaining: {self.format_time(state['remaining_time'])}")
        print("Use arrow keys to move")
        print("-" * 20)
        
        # Display grid
        for y in range(10):
            for x in range(10):
                ghost_here = (x == positions['ghost']['x'] and y == positions['ghost']['y'])
                player_here = (x == positions['player']['x'] and y == positions['player']['y'])
                
                if ghost_here and player_here:
                    print('X', end=' ')
                elif ghost_here:
                    print('G', end=' ')
                elif player_here:
                    print('P', end=' ')
                else:
                    print('.', end=' ')
            print()

        # Display game over message
        if state['game_over']:
            print("\nGAME OVER!")
            if state['winner'] == 'ghost':
                print("Ghost wins! The player was caught!")
            else:
                print("Player wins! They survived the full time!")
            print("\nPress 'q' to quit")

    def handle_input(self):
        while self.running and not self.game_over:
            try:
                if keyboard.is_pressed('up'):
                    self.client.send('up'.encode())
                    time.sleep(0.1)
                elif keyboard.is_pressed('down'):
                    self.client.send('down'.encode())
                    time.sleep(0.1)
                elif keyboard.is_pressed('left'):
                    self.client.send('left'.encode())
                    time.sleep(0.1)
                elif keyboard.is_pressed('right'):
                    self.client.send('right'.encode())
                    time.sleep(0.1)
                elif keyboard.is_pressed('q'):
                    self.running = False
                    break
                
                time.sleep(0.05)
            except:
                self.running = False
                break

    def start(self):
        receive_thread = threading.Thread(target=self.receive_state)
        receive_thread.daemon = True
        receive_thread.start()
        
        input_thread = threading.Thread(target=self.handle_input)
        input_thread.daemon = True
        input_thread.start()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
        
        self.client.close()

if __name__ == "__main__":
    client = GameClient()
    client.start()