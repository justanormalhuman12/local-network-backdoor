Local-Network Backdoor
-
Overview:
The Host-Receiver App consists of two Python scripts: host.py and receiver.py.

host.py : Acts as a client that connects to a server running receiver.py. It allows you to send commands to the server and can trigger popup windows on the client machine.
receiver.py: Acts as a server that listens for commands from the client and executes them. It sends the output of the executed commands back to the client.
How It Works

Client Script (host.py):
-
*Connects to the server via IP address and port.
*rovides a command input interface.
*Can execute commands on the server and display a popup window on the client machine using *the chat <message> command.

Server Script (receiver.py):
-
*Listens for incoming connections on a specified port.
*Executes commands received from the client.
*Sends command output back to the client.

How to Run the Scripts
-
1. Prepare the Environment
-Ensure Python is installed on both the server and client machines.
-The tkinter library is used for GUI popups in host.py. It comes with Python's standard library.
2. Running the Server (receiver.py)
-Open a terminal or command prompt on the server machine.
-Navigate to the directory containing receiver.py.
-Run the server script:
```python receiver.py```
4.The server will start listening for incoming connections on port 65432 (or the port you specify).

Running the Client (host.py)
-
-Open a terminal or command prompt on the client machine.
-Navigate to the directory containing 'host.py'
-Run the client script:
```python host.py```
-The client will connect to the server using the host's IP address and port 65432 (or the port you specify).

Using the Client
-
-Enter commands in the client interface to execute them on the server.
To display a popup window on the client machine, use the "chat <message>" command. For example:
```chat Hello,this is a test message```
-To disconnect the client, type exit and press Enter.

Example Workflow
-
1.Start the Server:
```python receiver.py```

2.Start the Client:
```python host.py```

3.Send a Command from the Client:
```dir  # On Windows ``` ```ls   # On Linux/Mac```

4.Trigger a Popup from the Client:
```chat This is a popup message```

5.Disconnect the Client:
```exit```

Notes
-
*Port and IP Address: Ensure the client connects to the correct IP address and port of the server. Modify the HOST and PORT variables in the scripts as needed.

*Firewall and Network: Ensure the port used by the server is open and not blocked by any firewall or network restrictions.

Troubleshooting
-
*No Response from Server: Verify that the server is running and listening on the correct port. Ensure the client is using the correct IP address.
*Popup Issues: Ensure tkinter is properly installed and configured on the client machine.



