import tkinter as tk
import random
import string

def generate_password():
    length = entry_length.get()

    if not length.isdigit() or int(length) <= 0:
        result_label.config(text="Enter a positive number")
        return

    length = int(length)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    result_label.config(text=password)

# GUI 
root = tk.Tk()
root.title("Password Generator")
root.geometry("280x150")

tk.Label(root, text="Password length:").pack(pady=5)
entry_length = tk.Entry(root)
entry_length.pack()

tk.Button(root, text="Generate", command=generate_password).pack(pady=8)
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

