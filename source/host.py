import socket

def main():
    host = '127.0.0.1'  # Change to the Receiver's IP if needed
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to Receiver.")
        
        while True:
            user_input = input("Enter command (prefix with 'command ', 'chat ', or 'screenshot' or 'cls'): ")
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            elif user_input.lower() == "cls":
                # Clear the console
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

            # Send the command to the Receiver
            client_socket.sendall(user_input.encode())
            response = client_socket.recv(4096).decode()
            print(f"Response from Receiver: {response}")

if __name__ == "__main__":
    main()
