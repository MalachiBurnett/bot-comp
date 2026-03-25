import tkinter as tk
from tkinter import messagebox, filedialog
import importlib.util
import os
import sys
from engine import SlideGame

class SlideGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Slide DevKit - Tester")
        self.game = SlideGame()
        self.selected_piece = None
        self.bot_module = None
        
        self.cell_size = 80
        self.canvas = tk.Canvas(root, width=6*self.cell_size, height=6*self.cell_size, bg="white")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.status_label = tk.Label(root, text="White's Turn", font=("Arial", 14))
        self.status_label.pack()
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Load Bot", command=self.load_bot).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Bot Move", command=self.make_bot_move).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_game).grid(row=0, column=2, padx=5)
        
        self.draw_board()

    def draw_board(self, winning_line=None):
        self.canvas.delete("all")
        for r in range(6):
            for c in range(6):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                fill_color = "#f0f0f0" if (r + c) % 2 == 0 else "#d0d0d0"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")
                
                piece = self.game.board[r][c]
                if piece != 0:
                    color = "white" if piece == 1 else "black"
                    outline = "red" if self.selected_piece == (r, c) else "black"
                    width = 3 if self.selected_piece == (r, c) else 1
                    
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill=color, outline=outline, width=width)
        
        if winning_line:
            for r, c in winning_line:
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=4)

    def on_click(self, event):
        c, r = event.x // self.cell_size, event.y // self.cell_size
        if not (0 <= r < 6 and 0 <= c < 6): return
        
        if self.selected_piece:
            sr, sc = self.selected_piece
            if (r, c) == (sr, sc):
                self.selected_piece = None
            else:
                # Try to determine direction from click
                dr, dc = r - sr, c - sc
                direction = None
                if dr == 0 and dc != 0:
                    direction = "RIGHT" if dc > 0 else "LEFT"
                elif dc == 0 and dr != 0:
                    direction = "DOWN" if dr > 0 else "UP"
                
                if direction and self.game.can_move(sr, sc, direction):
                    self.game.apply_move((sr, sc), direction)
                    self.selected_piece = None
                    self.after_move()
                else:
                    if self.game.board[r][c] == self.game.current_player:
                        self.selected_piece = (r, c)
            self.draw_board()
        else:
            if self.game.board[r][c] == self.game.current_player:
                self.selected_piece = (r, c)
                self.draw_board()

    def after_move(self):
        winner, line = self.game.check_win()
        if winner:
            self.status_label.config(text=f"{'White' if winner==1 else 'Black'} Wins!")
            self.draw_board(line)
            messagebox.showinfo("Game Over", f"{'White' if winner==1 else 'Black'} wins!")
        elif self.game.is_draw():
            self.status_label.config(text="Draw!")
            self.draw_board()
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            self.status_label.config(text=f"{'White' if self.game.current_player==1 else 'Black'}'s Turn")

    def reset_game(self):
        self.game = SlideGame()
        self.selected_piece = None
        self.status_label.config(text="White's Turn")
        self.draw_board()

    def load_bot(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            spec = importlib.util.spec_from_file_location("bot_module", file_path)
            self.bot_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.bot_module)
            messagebox.showinfo("Bot Loaded", f"Loaded {os.path.basename(file_path)}")

    def make_bot_move(self):
        if not self.bot_module:
            messagebox.showwarning("No Bot", "Please load a bot first.")
            return
        
        norm_board = self.game.get_normalized_board(self.game.current_player)
        try:
            move = self.bot_module.bot(norm_board)
            if move and self.game.can_move(move[0][0], move[0][1], move[1]):
                if self.game.board[move[0][0]][move[0][1]] == self.game.current_player:
                    self.game.apply_move(move[0], move[1])
                    self.after_move()
                    self.draw_board()
                else:
                    messagebox.showerror("Illegal Move", "Bot tried to move opponent's piece or empty square.")
            else:
                messagebox.showerror("Illegal Move", f"Bot returned invalid move: {move}")
        except Exception as e:
            messagebox.showerror("Bot Error", f"Bot crashed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SlideGUI(root)
    root.mainloop()
