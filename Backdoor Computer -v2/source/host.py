import socket
import os
import tkinter as tk
from tkinter import messagebox

# Host configuration
HOST = socket.gethostbyname(socket.gethostname())  # Automatically get the host's IP address
PORT = 65432  # Port to connect to

def show_popup(message):
    # Create a simple Tkinter popup window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Message from Host", message)
    root.destroy()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        while True:
            command = input("Enter command: ")
            if command.lower() == "exit":
                s.sendall(command.encode('utf-8'))
                break
            elif command.lower().startswith('chat '):
                # Trigger a popup window for 'chat' command
                message = command[5:].strip()  # Extract the message after 'chat'
                show_popup(message)
                continue  # No need to send the 'chat' command to the receiver
            else:
                s.sendall(command.encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
                print(f"Response: {data}")

if __name__ == "__main__":
    main()
