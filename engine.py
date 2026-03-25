import copy

class SlideGame:
    def __init__(self):
        # 0: Empty, 1: White, 2: Black
        # Setup according to rules:
        # Row 0: [Black, 0, White, Black, 0, White]
        # Row 1: [0, 0, 0, 0, 0, 0]
        # Row 2: [White, 0, 0, 0, 0, Black]
        # Row 3: [Black, 0, 0, 0, 0, White]
        # Row 4: [0, 0, 0, 0, 0, 0]
        # Row 5: [White, 0, Black, White, 0, Black]
        self.board = [
            [2, 0, 1, 2, 0, 1],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 2, 1, 0, 2]
        ]
        self.current_player = 1  # White moves first
        self.history = {}  # For 3-fold repetition
        self.record_state()

    def record_state(self):
        state = tuple(tuple(row) for row in self.board)
        self.history[state] = self.history.get(state, 0) + 1

    def get_legal_moves(self, player):
        moves = []
        for r in range(6):
            for c in range(6):
                if self.board[r][c] == player:
                    for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                        if self.can_move(r, c, direction):
                            moves.append(((r, c), direction))
        return moves

    def can_move(self, r, c, direction):
        dr, dc = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}[direction]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 6 and 0 <= nc < 6:
            return self.board[nr][nc] == 0
        return False

    def apply_move(self, pos, direction):
        r, c = pos
        player = self.board[r][c]
        dr, dc = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}[direction]
        
        self.board[r][c] = 0
        curr_r, curr_c = r, c
        while True:
            next_r, next_c = curr_r + dr, curr_c + dc
            if 0 <= next_r < 6 and 0 <= next_c < 6 and self.board[next_r][next_c] == 0:
                curr_r, curr_c = next_r, next_c
            else:
                break
        self.board[curr_r][curr_c] = player
        self.current_player = 3 - self.current_player
        self.record_state()

    def check_win(self):
        # Returns the winner (1 or 2) or None, and the winning line coordinates
        for r in range(6):
            for c in range(6):
                player = self.board[r][c]
                if player == 0:
                    continue
                
                for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    line = [(r, c)]
                    for i in range(1, 6):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < 6 and 0 <= nc < 6 and self.board[nr][nc] == player:
                            line.append((nr, nc))
                        else:
                            break
                    if len(line) >= 4:
                        return player, line
        return None, None

    def is_draw(self):
        # 3-fold repetition
        state = tuple(tuple(row) for row in self.board)
        if self.history.get(state, 0) >= 3:
            return True
        # No legal moves
        if not self.get_legal_moves(self.current_player):
            return True
        return False

    def get_normalized_board(self, player):
        # 0: empty, 1: opponent, 2: self
        normalized = []
        opponent = 3 - player
        for r in range(6):
            row = []
            for c in range(6):
                val = self.board[r][c]
                if val == 0:
                    row.append(0)
                elif val == player:
                    row.append(2)
                else:
                    row.append(1)
            normalized.append(row)
        return normalized
