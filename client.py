import socket
import sys

HOST = 'localhost'
PORT = 65432


def print_board(board):
    for i in range(0, 9, 3):
        row = ' | '.join(board[i:i+3])
        print(row)
        if i < 6:
            print('-' * 5)


def recv_line(sock):
    """Receive bytes from a socket until a newline character."""
    chunks = []
    while True:
        chunk = sock.recv(1)
        if not chunk:
            return None
        if chunk == b'\n':
            break
        chunks.append(chunk)
    return b''.join(chunks).decode()


def main():
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = HOST
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, PORT))
        symbol = None
        while True:
            line = recv_line(s)
            if line is None:
                break
            if line.startswith('START'):
                symbol = line.split()[1]
                print('You are', symbol)
            elif line.startswith('BOARD'):
                board_state = line.split()[1]
                board = [' ' if ch == '.' else ch for ch in board_state]
                print_board(board)
            elif line.startswith('TURN'):
                turn = line.split()[1]
                if turn == symbol:
                    print("Your turn")
            elif line == 'YOURMOVE':
                move = input('Enter position (1-9) using numpad layout: ')
                s.sendall((move + '\n').encode())
            elif line == 'INVALID':
                print('Invalid move, try again')
            elif line.startswith('WIN'):
                winner = line.split()[1]
                if winner == symbol:
                    print('You win!')
                else:
                    print('You lose.')
                input('Game over. Press Enter to exit.')
                return
            elif line == 'DRAW':
                print('Draw!')
                input('Game over. Press Enter to exit.')
                return


if __name__ == '__main__':
    main()
