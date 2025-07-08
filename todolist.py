import tkinter as tk
from tkinter import ttk, messagebox
from uuid import uuid4
import json, os
from datetime import datetime
try:
    from tkcalendar import DateEntry          # pip install tkcalendar
except ImportError:
    raise ImportError("Install tkcalendar:  pip install tkcalendar")

DATA_FILE = "tasks.json"

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To‑Do – Get Things Done!")
        self.geometry("620x500")
        self.resizable(False, False)

        self.tasks = {}
        self.create_banner()
        self.create_start_screen()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        if os.path.exists(DATA_FILE):
            self.load_tasks()

    def create_banner(self):
        banner = tk.Frame(self, bg="#4c4c6d")
        banner.pack(fill="x")
        tk.Label(banner, text="TO‑DO", fg="white", bg="#4c4c6d",
                 font=("Helvetica", 24, "bold")).pack()
        tk.Label(banner, text="“Small steps, big results.”",
                 fg="#f1f1f1", bg="#4c4c6d", font=("Helvetica", 10, "italic")).pack(pady=(0,6))

    def create_start_screen(self):
        self.start_btn = ttk.Button(self, text="Let’s Start!", command=self.show_manager)
        self.start_btn.place(relx=0.5, rely=0.5, anchor="center")

    def show_manager(self):
        self.start_btn.destroy()
        frm = tk.Frame(self)
        frm.pack(pady=10, fill="x")

        # Input row
        tk.Label(frm, text="Task").grid(row=0, column=0, sticky="w", padx=5)
        self.title_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.title_var, width=28).grid(row=0, column=1, padx=5)

        tk.Label(frm, text="Deadline").grid(row=0, column=2, sticky="w")
        self.date_var = tk.StringVar()
        DateEntry(frm, textvariable=self.date_var, width=12, date_pattern='yyyy-mm-dd').grid(row=0, column=3, padx=5)

        self.done_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text="Done?", variable=self.done_var).grid(row=0, column=4, padx=5)

        ttk.Button(frm, text="Add", width=9, command=self.add_task).grid(row=0, column=5, padx=5)

        cols = ("Title", "Deadline", "Status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by(c, False))
            self.tree.column(col, width=180 if col=="Title" else 100, anchor="center")
        self.tree.pack(pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.populate_inputs)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Update", width=10, command=self.update_task).grid(row=0, column=0, padx=3)
        ttk.Button(btn_frame, text="Delete", width=10, command=self.delete_task).grid(row=0, column=1, padx=3)
        ttk.Button(btn_frame, text="Mark Done", width=10, command=self.mark_done).grid(row=0, column=2, padx=3)
        ttk.Button(btn_frame, text="Clear All", width=10, command=self.clear_all).grid(row=0, column=3, padx=3)

        self.refresh_tree()

    def add_task(self):
        title = self.title_var.get().strip()
        deadline = self.date_var.get()
        if not title:
            messagebox.showerror("Missing title", "Please enter a task description.")
            return
        tid = str(uuid4())
        self.tasks[tid] = {"title": title,
                           "deadline": deadline,
                           "done": self.done_var.get()}
        self.save_tasks()
        self.refresh_tree()
        self.title_var.set("")
        self.done_var.set(False)

    def populate_inputs(self, _):
        sel = self.tree.selection()
        if not sel: return
        tid = sel[0]
        t = self.tasks[tid]
        self.title_var.set(t["title"])
        self.date_var.set(t["deadline"])
        self.done_var.set(t["done"])

    def update_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select task", "Choose a task to update.")
            return
        tid = sel[0]
        self.tasks[tid]["title"] = self.title_var.get().strip()
        self.tasks[tid]["deadline"] = self.date_var.get()
        self.tasks[tid]["done"] = self.done_var.get()
        self.save_tasks()
        self.refresh_tree()

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select task", "Choose a task to delete.")
            return
        for tid in sel:
            del self.tasks[tid]
        self.save_tasks()
        self.refresh_tree()

    def mark_done(self):
        sel = self.tree.selection()
        if not sel: return
        for tid in sel:
            self.tasks[tid]["done"] = True
        self.save_tasks()
        self.refresh_tree()

    def clear_all(self):
        if messagebox.askyesno("Clear everything?", "Are you sure?"):
            self.tasks.clear()
            self.save_tasks()
            self.refresh_tree()

    # ---------- UTILITIES ----------
    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        today = datetime.today().date()
        for tid, task in self.tasks.items():
            status = "Done" if task["done"] else "Pending"
            self.tree.insert("", "end", iid=tid,
                             values=(task["title"], task["deadline"], status))
            if not task["done"] and task["deadline"]:
                try:
                    dl = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                    if dl < today:
                        self.tree.item(tid, tags=("overdue",))
                except ValueError:
                    pass
        self.tree.tag_configure("overdue", foreground="red")

    def sort_by(self, col, descending):
        idx = {"Title": 0, "Deadline": 1, "Status": 2}[col]
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=descending, key=lambda t: t[0])
        for i, (_, k) in enumerate(data):
            self.tree.move(k, "", i)
        # toggle next time
        self.tree.heading(col, command=lambda c=col: self.sort_by(c, not descending))

    def load_tasks(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except Exception:
            self.tasks = {}

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def on_close(self):
        self.save_tasks()
        self.destroy()

if __name__ == "__main__":
    TodoApp().mainloop()
