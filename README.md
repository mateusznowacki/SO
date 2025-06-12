# Tic-Tac-Toe Network Game

Two simple Python scripts provide a minimal network implementation of tic-tac-toe.
One acts as the server and manages the game logic, the other is a client that
connects via TCP.

## Files
- `server.py` – waits for two clients, coordinates turns and checks for a win.
- `client.py` – connects to the server and lets a player choose moves.

## Running the game
Start the server in one terminal. You can optionally choose the TCP port (default 65432):

```bash
python server.py            # use default port 65432
python server.py 12345      # choose a custom port
```

Then start two clients (in separate terminals). Pass the host and port if you changed them:

```bash
python client.py                     # connect to localhost:65432
# Optionally specify server address and port
python client.py 127.0.0.1 12345
```

Moves are entered using the standard numpad layout:

```
7 | 8 | 9
---------
4 | 5 | 6
---------
1 | 2 | 3
```

The server keeps both players updated with simple text messages. Empty cells
are transmitted as a dot (`.`) and displayed as blanks by the client. When a
win or a draw occurs the server notifies both clients.

To verify the scripts are syntactically correct you can run:

```bash
python -m py_compile server.py client.py
```
