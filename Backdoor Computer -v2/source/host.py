import socket
import os
import tkinter as tk
from tkinter import messagebox

# Host configuration
HOST = socket.gethostbyname(socket.gethostname())  # Automatically get the host's IP address
PORT = 65432  # Port to connect to

def show_popup(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Message from Host", message)
    root.destroy()

def connect_to_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        return s
    except socket.error as e:
        print(f"Connection error: {e}")
        return None

def handle_command(command, socket_connection):
    if command.lower() == "exit":
        socket_connection.sendall(command.encode('utf-8'))
        return False
    elif command.lower().startswith('chat '):
        message = command[5:].strip()
        show_popup(message)
    else:
        try:
            socket_connection.sendall(command.encode('utf-8'))
            data = socket_connection.recv(1024).decode('utf-8')
            print(f"Response: {data}")
        except socket.error as e:
            print(f"Communication error: {e}")
            return False
    return True

def main():
    s = connect_to_server()
    if s is None:
        print("Exiting due to connection failure.")
        return
    
    with s:
        while True:
            command = input("Enter command: ").strip()
            if not command:
                print("Please enter a valid command.")
                continue
            
            if not handle_command(command, s):
                break

if __name__ == "__main__":
    main()
