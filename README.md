# Tic-Tac-Toe Network Game

Two simple Python scripts provide a minimal network implementation of tic-tac-toe.
One acts as the server and manages the game logic, the other is a client that
connects via TCP.

## Files
- `server.py` – waits for two clients, coordinates turns and checks for a win.
- `client.py` – connects to the server and lets a player choose moves.

## Running the game
Start the server in one terminal:

```bash
python server.py
```

Then start two clients (in separate terminals):

```bash
python client.py
# Optionally specify server address
python client.py 127.0.0.1
```

Moves are entered as numbers 1–9 according to the positions:

```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

The server keeps both players updated with simple text messages. Empty cells
are transmitted as a dot (`.`) and displayed as blanks by the client. When a
win or a draw occurs the server notifies both clients.

To verify the scripts are syntactically correct you can run:

```bash
python -m py_compile server.py client.py
```
