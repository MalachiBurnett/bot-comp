import random

def bot(gamestate):
    """
    Randomly chooses a legal move.
    gamestate: 0=empty, 1=opponent, 2=self
    """
    legal_moves = []
    for r in range(6):
        for c in range(6):
            if gamestate[r][c] == 2:  # Self
                for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    dr, dc = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}[direction]
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 6 and 0 <= nc < 6 and gamestate[nr][nc] == 0:
                        legal_moves.append(((r, c), direction))
    
    if not legal_moves:
        return None
    return random.choice(legal_moves)
