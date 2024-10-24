import os
import socket
import tempfile
import threading
from PIL import ImageGrab
import tkinter as tk
from tkinter import messagebox
import time

def display_popup(message):
    """Display a message in a popup window."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Message from Host", message)
    root.destroy()

def open_image(file_path):
    """Open the image using the default image viewer."""
    os.startfile(file_path)

def handle_client(conn):
    """Handle commands from the Host."""
    while True:
        command = conn.recv(1024).decode()
        if not command:
            break
        
        if command.startswith("command "):
            # Execute system command
            result = os.popen(command[len("command "):]).read()
            conn.sendall(result.encode())
        elif command.startswith("chat "):
            # Display chat message in a new thread
            message = command[len("chat "):]
            threading.Thread(target=display_popup, args=(message,)).start()
            conn.sendall(b'Message displayed')
        elif command.lower() == "screenshot":
            # Capture screenshot and save it to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                screenshot_path = temp_file.name
                ImageGrab.grab().save(screenshot_path)
                
                # Open the screenshot after saving
                open_image(screenshot_path)

            # Wait for a brief moment to ensure the image viewer has opened
            time.sleep(1)

            # Delete the temporary screenshot file
            try:
                os.remove(screenshot_path)
                conn.sendall(b"Screenshot captured and displayed. Temporary file deleted.")
            except Exception as e:
                conn.sendall(f"Failed to delete screenshot: {str(e)}".encode())
        elif command.lower() == "cls":
            # Clear the console
            os.system('cls' if os.name == 'nt' else 'clear')
            conn.sendall(b"Console cleared.")
        else:
            conn.sendall(b'Invalid command')

def main():
    host = '127.0.0.1'  # Change to your IP if needed
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening for connections on {host}:{port}...")
        
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()
