import socket  # Import the socket module

def client_program():
    host = "127.0.0.1"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(message)

            # Handle difficulty voting
            if "Choose difficulty" in message:
                user_input = input("Enter difficulty (easy, medium, hard): ").strip().lower()
                while user_input not in ["easy", "medium", "hard"]:
                    print("Invalid input! Please choose between 'easy', 'medium', or 'hard'.")
                    user_input = input("Enter difficulty (easy, medium, hard): ").strip().lower()
                client_socket.send(user_input.encode())

            # Handle moves or nickname input
            elif "Enter" in message:
                user_input = input()
                client_socket.send(user_input.encode())

    except KeyboardInterrupt:
        print("Disconnected from server.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client_program()
