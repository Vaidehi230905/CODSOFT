import tkinter as tk
import random

CHOICES = ("Rock", "Paper", "Scissors")
BTN_COLORS = {
    "Rock":     ("#6d6d6d", "#8f8f8f"),
    "Paper":    ("#4aa3ff", "#6bb4ff"),
    "Scissors": ("#ff944a", "#ffab73"),
}
BG_MAIN = "#222831"
FG_TEXT = "#eeeeee"

def decide_winner(user, comp):
    if user == comp:
        return "It's a tie!", "tie"
    wins = {("Rock", "Scissors"), ("Scissors", "Paper"), ("Paper", "Rock")}
    return ("You win!", "user") if (user, comp) in wins else ("Computer wins!", "computer")

def color_for(outcome):
    return {"user": "#4CAF50", "computer": "#F44336", "tie": "#03A9F4"}.get(outcome, FG_TEXT)

root = tk.Tk()
root.title("Rock Paper Scissors")
root.configure(bg=BG_MAIN)

tk.Label(root, text="Rock  Paper  Scissors", font=("Helvetica", 24, "bold"),
         fg="#00e0ff", bg=BG_MAIN).pack(pady=(15, 4))

tk.Label(root, text="INSTRUCTIONS\n1.Click a button to make your move.\n2.Rock beats scissors, scissors beat paper, and paper beats rock.", font=("Helvetica", 13),
         fg=FG_TEXT, bg=BG_MAIN).pack(pady=(0, 10))


user_score = tk.IntVar(value=0)
comp_score = tk.IntVar(value=0)
score_lbl = tk.Label(root, font=("Helvetica", 12, "bold"),
                     fg="#ffd369", bg=BG_MAIN)
score_lbl.pack()
score_lbl.config(text=f"Score — You: {user_score.get()}   Computer: {comp_score.get()}")

choices_var = tk.StringVar(value="—")
result_var  = tk.StringVar(value="")

tk.Label(root, textvariable=choices_var, font=("Helvetica", 12),
         fg="#ffdc5e", bg=BG_MAIN).pack(pady=(12, 2))
result_lbl = tk.Label(root, textvariable=result_var, font=("Helvetica", 16, "bold"),
                      fg=FG_TEXT, bg=BG_MAIN)
result_lbl.pack(pady=(0, 8))

btn_frame = tk.Frame(root, bg=BG_MAIN)
btn_frame.pack(pady=6)

def make_btn(choice):
    bg_norm, bg_hover = BTN_COLORS[choice]
    btn = tk.Button(btn_frame, text=choice, width=12, height=2,
                    font=("Helvetica", 12, "bold"),
                    fg=FG_TEXT, bg=bg_norm,
                    activebackground=bg_hover,
                    command=lambda c=choice: play(c),
                    relief="raised", bd=3)
    btn.bind("<Enter>", lambda e: btn.config(bg=bg_hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_norm))
    return btn

for i, c in enumerate(CHOICES):
    make_btn(c).grid(row=0, column=i, padx=8, pady=5)

# game logic
def play(user_choice):
    comp_choice = random.choice(CHOICES)
    message, outcome = decide_winner(user_choice, comp_choice)

    if outcome == "user":
        user_score.set(user_score.get() + 1)
    elif outcome == "computer":
        comp_score.set(comp_score.get() + 1)

    choices_var.set(f"You chose: {user_choice}   |   Computer chose: {comp_choice}")
    result_var.set(message)
    result_lbl.config(fg=color_for(outcome))
    score_lbl.config(text=f"Score — You: {user_score.get()}   Computer: {comp_score.get()}")

# play‑again button
def play_again():
    choices_var.set("—")
    result_var.set("")
    result_lbl.config(fg=FG_TEXT)

tk.Button(root, text="Play Again", width=36, height=1,
          font=("Helvetica", 11, "bold"),
          fg=FG_TEXT, bg="#393E46",
          activebackground="#4e545e",
          command=play_again).pack(pady=(0, 15))

root.mainloop()
