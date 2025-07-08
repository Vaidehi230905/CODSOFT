import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        op = operator.get()

        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
                return
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Invalid operator selected.")
            return

        result_label.config(text=f"Result: {num1} {op} {num2} = {result}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# GUI 
root = tk.Tk()
root.title("Simple Calculator")

tk.Label(root, text="First Number").grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Second Number").grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5)

# Operator selection
tk.Label(root, text="Operation (+ - * /)").grid(row=2, column=0, padx=10, pady=5)
operator = tk.StringVar()
operator_entry = tk.Entry(root, textvariable=operator)
operator_entry.grid(row=2, column=1, padx=10, pady=5)

# Calculate button
tk.Button(root, text="Calculate", command=calculate).grid(row=3, column=0, columnspan=2, pady=10)

# Result 
result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
