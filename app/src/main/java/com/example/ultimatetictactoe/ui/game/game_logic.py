PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
DRAW = 'D'

class UltimateTicTacToe:
    def __init__(self):
        self.local_boards = [
            [[[EMPTY for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)
        ]
        self.meta_board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_X
        self.next_board_coords = None
        self.game_winner = None

    def _check_winner(self, board_3x3):
        for row in board_3x3:
            if row[0] == row[1] == row[2] and row[0] != EMPTY:
                return row[0]
        for col in range(3):
            if board_3x3[0][col] == board_3x3[1][col] == board_3x3[2][col] and board_3x3[0][col] != EMPTY:
                return board_3x3[0][col]
        if board_3x3[0][0] == board_3x3[1][1] == board_3x3[2][2] and board_3x3[0][0] != EMPTY:
            return board_3x3[0][0]
        if board_3x3[0][2] == board_3x3[1][1] == board_3x3[2][0] and board_3x3[1][1] != EMPTY:
            return board_3x3[1][1]
        if all(cell != EMPTY for row in board_3x3 for cell in row):
            return DRAW
        return None

    def get_game_status(self):
        if self.game_winner == PLAYER_X:
            return 'X_WINS'
        if self.game_winner == PLAYER_O:
            return 'O_WINS'
        if self.game_winner == DRAW:
            return 'DRAW'
        meta_status = self._check_winner(self.meta_board)
        if meta_status == DRAW:
            self.game_winner = DRAW
            return 'DRAW'
        return 'IN_PROGRESS'

    def _is_valid_move(self, board_row, board_col, cell_row, cell_col):
        if self.game_winner:
            return False
        if not (0 <= board_row < 3 and 0 <= board_col < 3 and
                0 <= cell_row < 3 and 0 <= cell_col < 3):
            return False
        if self.next_board_coords:
            if (board_row, board_col) != self.next_board_coords:
                return False
        if self.meta_board[board_row][board_col] != EMPTY:
            return False
        if self.local_boards[board_row][board_col][cell_row][cell_col] != EMPTY:
            return False
        return True

    def get_valid_moves(self):
        if self.get_game_status() != 'IN_PROGRESS':
            return []
        moves = []
        if self.next_board_coords:
            br, bc = self.next_board_coords
            if self.meta_board[br][bc] == EMPTY:
                for cr in range(3):
                    for cc in range(3):
                        if self.local_boards[br][bc][cr][cc] == EMPTY:
                            moves.append((br, bc, cr, cc))
        if not moves:
            for br in range(3):
                for bc in range(3):
                    if self.meta_board[br][bc] == EMPTY:
                        for cr in range(3):
                            for cc in range(3):
                                if self.local_boards[br][bc][cr][cc] == EMPTY:
                                    moves.append((br, bc, cr, cc))
        return moves

    def make_move(self, board_row, board_col, cell_row, cell_col):
        if not self._is_valid_move(board_row, board_col, cell_row, cell_col):
            print(f"Invalid move: ({board_row}, {board_col}, {cell_row}, {cell_col})")
            return False
        self.local_boards[board_row][board_col][cell_row][cell_col] = self.current_player
        local_board = self.local_boards[board_row][board_col]
        local_winner = self._check_winner(local_board)
        if local_winner:
            self.meta_board[board_row][board_col] = local_winner
        global_winner = self._check_winner(self.meta_board)
        if global_winner:
            self.game_winner = global_winner
            return True
        next_br, next_bc = cell_row, cell_col
        if self.meta_board[next_br][next_bc] != EMPTY:
            self.next_board_coords = None
        else:
            self.next_board_coords = (next_br, next_bc)
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        return True

    def print_board(self):
        print("-" * 25)
        for meta_row in range(3):
            for cell_row in range(3):
                line = ""
                for meta_col in range(3):
                    for cell_col in range(3):
                        cell = self.local_boards[meta_row][meta_col][cell_row][cell_col]
                        line += cell
                    if meta_col < 2:
                        line += " | "
                print(line)
            if meta_row < 2:
                print("---------+---------+---------")
        print("\nMeta Board:")
        for row in self.meta_board:
            print(f" {row[0] if row[0] != EMPTY else '.'} | {row[1] if row[1] != EMPTY else '.'} | {row[2] if row[2] != EMPTY else '.'} ")
        print(f"\nCurrent Player: {self.current_player}")
        if self.next_board_coords:
            print(f"Next must play in board: {self.next_board_coords}")
        else:
            print("Next move is: Free Play")
        print(f"Status: {self.get_game_status()}")
        print("-" * 25)

if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.print_board()
    print("\n--- Move 1: X at (1, 1, 1, 1) ---")
    game.make_move(1, 1, 1, 1)
    game.print_board()
    print("\n--- Move 2: O at (1, 1, 0, 0) ---")
    game.make_move(1, 1, 0, 0)
    game.print_board()
    print("\n--- Move 3: X at (0, 0, 0, 0) ---")
    game.make_move(0, 0, 0, 0)
    game.print_board()
    print("\n--- Simulating a local win for X... ---")
    game = UltimateTicTacToe()
    game.make_move(0, 0, 0, 0)
    game.make_move(0, 0, 1, 1)
    game.make_move(1, 1, 0, 0)
    game.make_move(0, 0, 0, 1)
    game.make_move(0, 1, 0, 0)
    game.make_move(0, 0, 0, 2)
    print("Board state before X wins a local board:")
    game.print_board()
    print("\n--- Move: X at (0, 2, 0, 0) ---")
    game.make_move(0, 2, 0, 0)
    print("X played. O must play in board (0,0).")
    game.print_board()
    print(f"\n--- Move: O plays at (0, 0, 2, 2). This move is invalid! ---")
    valid = game.make_move(0, 0, 2, 2)
    print(f"Move successful: {valid}")
    if not valid:
        print("Move was correctly rejected.")
    print("\n--- Let's get valid moves for O ---")
    valid_moves = game.get_valid_moves()
    print(f"Valid moves ({len(valid_moves)}): {valid_moves}")
    game.make_move(0, 0, 2, 2)
    print("\nO made a valid move in board (0,0).")
    game.print_board()
    print("\n--- Move: X at (2, 2, 1, 1) ---")
    game.make_move(2, 2, 1, 1)
    game.print_board()
    print("\n--- Simulating X winning board (1,1) ---")
    game.current_player = PLAYER_X
    game.next_board_coords = (1, 1)
    game.make_move(1, 1, 0, 1)
    game.make_move(0, 1, 1, 1)
    game.current_player = PLAYER_X
    game.next_board_coords = (1, 1)
    game.make_move(1, 1, 0, 2)
    print("X won board (1,1)!")
    game.print_board()
    print(f"O must play in {game.next_board_coords}")
    game.make_move(0, 2, 2, 2)
    print(f"X must play in {game.next_board_coords}")
    game.print_board()
    game.make_move(2, 2, 1, 1)
    print("X played at (2,2,1,1).")
    print(f"Next board *should* be (1,1), but meta_board[1][1] is '{game.meta_board[1][1]}'")
    print(f"Therefore, next_board_coords is: {game.next_board_coords}")
    print("It's FREE PLAY for O!")
    game.print_board()
    print("\nValid moves for O (free play):")
    moves = game.get_valid_moves()
    print(f"There are {len(moves)} valid moves.")