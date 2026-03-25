import os
import importlib.util
import time
import concurrent.futures
from engine import SlideGame

SUBMISSIONS_DIR = "submissions"
TIMEOUT = 2.0  # seconds

def run_bot_safe(bot_func, gamestate):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.submit(bot_func, gamestate)
        try:
            return future.result(timeout=TIMEOUT)
        except concurrent.futures.TimeoutError:
            return "TIMEOUT"
        except Exception as e:
            return f"CRASH: {e}"

# Note: multiprocessing with loaded modules is tricky. 
# For a DevKit, we'll use a simpler approach: 
# Execute the bot function in a separate process by passing the code or path.
# However, for brevity and local testing, I'll implement a simple version here.

def get_move(bot_module, gamestate):
    # This is a simplified wrapper. In a real tournament, you'd use a separate process.
    try:
        start_time = time.time()
        move = bot_module.bot(gamestate)
        if time.time() - start_time > TIMEOUT:
            return "TIMEOUT"
        return move
    except Exception as e:
        return f"CRASH: {e}"

def play_match(bot1, bot2):
    # bot1 is White, bot2 is Black
    game = SlideGame()
    bots = {1: bot1, 2: bot2}
    
    while True:
        player = game.current_player
        norm_board = game.get_normalized_board(player)
        move = get_move(bots[player], norm_board)
        
        if isinstance(move, str):
            # Error (TIMEOUT, CRASH)
            return 3 - player, move # Winner is the other player
        
        # Validate move
        try:
            pos, direction = move
            r, c = pos
            if not (0 <= r < 6 and 0 <= c < 6) or game.board[r][c] != player or not game.can_move(r, c, direction):
                return 3 - player, "ILLEGAL_MOVE"
            
            game.apply_move(pos, direction)
        except:
            return 3 - player, "INVALID_FORMAT"
        
        winner, _ = game.check_win()
        if winner:
            return winner, "WIN"
        
        if game.is_draw():
            return 0, "DRAW"

def load_submissions():
    if not os.path.exists(SUBMISSIONS_DIR):
        os.makedirs(SUBMISSIONS_DIR)
        return {}
    
    bots = {}
    for entry in os.scandir(SUBMISSIONS_DIR):
        if entry.is_dir():
            bot_path = os.path.join(entry.path, "bot.py")
            info_path = os.path.join(entry.path, "info.txt")
            if os.path.exists(bot_path):
                spec = importlib.util.spec_from_file_location(f"bot_{entry.name}", bot_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                name = entry.name
                if os.path.exists(info_path):
                    with open(info_path, 'r') as f:
                        name = f.readline().strip() or entry.name
                
                bots[entry.name] = {"module": module, "name": name}
    return bots

def run_tournament():
    bots_dict = load_submissions()
    if not bots_dict:
        print("No bots found in /submissions. Create subfolders with bot.py and info.txt.")
        return

    bot_keys = list(bots_dict.keys())
    scores = {key: 0 for key in bot_keys}
    
    print(f"Starting tournament with {len(bot_keys)} bots...")
    
    for i in range(len(bot_keys)):
        for j in range(len(bot_keys)):
            if i == j: continue
            
            p1_key = bot_keys[i]
            p2_key = bot_keys[j]
            
            print(f"Match: {bots_dict[p1_key]['name']} (White) vs {bots_dict[p2_key]['name']} (Black)...", end=" ")
            winner_idx, reason = play_match(bots_dict[p1_key]['module'], bots_dict[p2_key]['module'])
            
            if winner_idx == 1:
                scores[p1_key] += 3
                print(f"Winner: {bots_dict[p1_key]['name']} ({reason})")
            elif winner_idx == 2:
                scores[p2_key] += 3
                print(f"Winner: {bots_dict[p2_key]['name']} ({reason})")
            else:
                scores[p1_key] += 1
                scores[p2_key] += 1
                print("Draw")
                
    print("\nFinal Results:")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for key, score in sorted_scores:
        print(f"{bots_dict[key]['name']}: {score} points")

if __name__ == "__main__":
    run_tournament()
