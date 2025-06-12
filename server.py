import socket

HOST = '0.0.0.0'
PORT = 65432


def check_winner(board):
    winning_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_combos:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    if ' ' not in board:
        return 'draw'
    return None


def broadcast(conns, message):
    """Send the same line of text to multiple connections."""
    data = (message + "\n").encode()
    for conn in conns:
        conn.sendall(data)


def recv_line(conn):
    """Receive bytes from a socket until a newline is found."""
    chunks = []
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None
        if chunk == b"\n":
            break
        chunks.append(chunk)
    return b"".join(chunks).decode()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Waiting for players on', PORT)
        conn1, addr1 = s.accept()
        print('Player 1 connected from', addr1)
        conn1.sendall(b'START X\n')
        conn2, addr2 = s.accept()
        print('Player 2 connected from', addr2)
        conn2.sendall(b'START O\n')

        board = [' '] * 9
        current = conn1
        symbol = 'X'

        while True:
            broadcast((conn1, conn2), 'BOARD ' + ''.join(board))
            broadcast((conn1, conn2), f'TURN {symbol}')
            current.sendall(b'YOURMOVE\n')
            line = recv_line(current)
            if line is None:
                break
            try:
                move = int(line.strip()) - 1
            except ValueError:
                current.sendall(b'INVALID\n')
                continue
            if move < 0 or move > 8 or board[move] != ' ':
                current.sendall(b'INVALID\n')
                continue
            board[move] = symbol
            winner = check_winner(board)
            if winner:
                broadcast((conn1, conn2), 'BOARD ' + ''.join(board))
                if winner == 'draw':
                    broadcast((conn1, conn2), 'DRAW')
                else:
                    broadcast((conn1, conn2), f'WIN {winner}')
                break
            current = conn2 if current is conn1 else conn1
            symbol = 'O' if symbol == 'X' else 'X'

        conn1.close()
        conn2.close()


if __name__ == '__main__':
    main()
