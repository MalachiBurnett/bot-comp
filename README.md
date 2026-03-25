# Slide Bot Competition - DevKit

Welcome to the **Slide** Bot-Building Competition! This kit contains everything you need to develop, test, and submit your bot. if you would like to play the game first, you can do so at https://slide.wiizardsoftware.uk/

### Submissions
once you have perfected your bot, please put it into a folder with your bot.py, any other files your bot includes, and an info.txt containing:
your bots nickname,
your name,
your username on slide.wiizardsoftware.uk,
and your contact info in case you win.

then you can either zip the folder and email it to me at maliburnett@icloud.com or you can put it on a github repositiory (either unlisted or public) as a branch of this repository if its public or send a link via email if its unlisted.

### prize
there will be a £5 cash prize awarded to the bot that wins the most games. in the case of a tie between bots, the creators of the bots can play a game of chess on chess.com to decide who gets the prize money. if it turns out that this game can be solved and played perfectly such that one colour can alway win, the first person to prove this will be awarded the cash prize instead and the competition wont happen.

## Game Rules
**Slide** is a 6x6 strategy game where pieces slide until they hit an obstacle.

### Setup
The board starts with 12 pieces (6 White, 6 Black) in the following configuration:
- Row 0: [Black, empty, White, Black, empty, White]
- Row 2: [White, empty, empty, empty, empty, Black]
- Row 3: [Black, empty, empty, empty, empty, White]
- Row 5: [White, empty, Black, White, empty, Black]

### Movement (The Slide)
- Pieces move orthogonally (**UP**, **DOWN**, **LEFT**, **RIGHT**).
- A piece **must** slide until it hits a wall or another piece. It cannot stop early or jump over pieces.
- White moves first.

### Winning
- The first player to align **4 or more** pieces in a continuous straight line (Horizontal, Vertical, or Diagonal) wins.

### Draws
- **3-fold repetition**: If the exact board state occurs 3 times.
- **No legal moves**: If a player has no pieces that can move.

---

## Technical Details

### Bot Interface
Your bot must be a Python file named `bot.py` containing a function:
```python
def bot(gamestate):
    # gamestate: 6x6 nested list
    # 0 = empty, 1 = opponent, 2 = self
    return ((row, col), "DIRECTION")
```
- **Normalized View**: Regardless of whether you are White or Black, your pieces are always represented as `2` and your opponent's as `1`.
- **Directions**: `"UP"`, `"DOWN"`, `"LEFT"`, `"RIGHT"`.

### Files in DevKit
- `engine.py`: The core game logic. Do not modify if you want to make sure your bot functions exactly as you intend to in the competition.
- `bot_template.py`: A starting point for your bot.
- `gui_tester.py`: A GUI to play manually or test your bot against yourself or others.
- `judge.py`: Runs a local tournament between all bots in the `submissions/` folder.
- `random_bot.py`: A simple bot that makes random legal moves.

### How to Test (Local)
1. Run `python gui_tester.py`.
2. Click "Load Bot" and select your `bot.py`.
3. Click "Bot Move" to see your bot in action.

the gui_tester is a simple app for you to play against your bot as a human.

### How to Test (Docker)
If you prefer to run the tournament judge in a container:
1. Ensure Docker and Docker Compose are installed.
2. Run `docker-compose up --build`.
This will build the image and execute a Round Robin tournament between all bots in your `submissions/` folder.

---

## Tournament Rules
- **Environment**: If running via Docker, your bot will be executed in a Python 3.10 environment.
- **Time Limit**: Your bot has **2 seconds** per move.
- **Illegal Moves**: If your bot returns an illegal move, crashes, or times out, it loses the match immediately.
- **Format**: Round Robin (each bot plays every other bot twice: once as White, once as Black).
- **Scoring**: 3 points for a win, 1 for a draw, 0 for a loss.

---

### a note on https://slide.wiizardsoftware.uk/
Please dont flood this site with your bots. it makes the game unfun for other players. whilst i cannot technically stop you from doing this, i just ask that you conider the fact that this is running on a server on my home wifi and i dont want to have to shut down the site because too many people are just bots. thank you for participating in this competition and may the best bot win.
