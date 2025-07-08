import tkinter as tk
from tkinter import messagebox
import json, os
from uuid import uuid4

DATA_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_contacts(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class ContactBookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.colors = {
            "bg": "#eaf2ff", "frame": "#ffffff", "accent": "#4f90ff",
            "accent_dark": "#3677ea", "accent_light": "#b9d3ff",
            "input_bg": "#f7fbff", "text": "#2f2f2f"
        }
        self.title("Contact Book")
        self.geometry("680x420")
        self.configure(bg=self.colors["bg"])
        self.resizable(False, False)
        self.data = load_contacts()
        self.build_main_ui()

    def build_main_ui(self):
        tk.Label(self, text="Contact Book", font=("Helvetica", 20, "bold"),
                 bg=self.colors["accent"], fg="white").pack(fill="x")

        main = tk.Frame(self, bg=self.colors["bg"])
        main.pack(expand=True, fill="both", padx=10, pady=10)

        left = tk.Frame(main, bg=self.colors["frame"])
        left.pack(side="left", fill="y", padx=(0, 10))

        self.search_var = tk.StringVar()
        tk.Entry(left, textvariable=self.search_var, width=24, font=("Helvetica", 11),
                 bg=self.colors["input_bg"], relief="flat").pack(padx=10, pady=(10, 4))
        tk.Button(left, text="🔍 Search", bg=self.colors["accent"], fg="white",
                  activebackground=self.colors["accent_dark"], borderwidth=0,
                  command=self.refresh_list).pack(pady=(0, 6))

        self.listbox = tk.Listbox(left, width=28, height=16, bg=self.colors["input_bg"],
                                  fg=self.colors["text"], font=("Consolas", 10),
                                  relief="flat", selectbackground=self.colors["accent_light"])
        self.listbox.pack(padx=10, pady=(0, 10))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        right = tk.Frame(main, bg=self.colors["frame"])
        right.pack(side="left", fill="both", expand=True)

        lbl = dict(bg=self.colors["frame"], fg=self.colors["text"],
                   font=("Helvetica", 10, "bold"), anchor="w")
        ent = dict(width=30, bg=self.colors["input_bg"],
                   relief="flat", font=("Helvetica", 10))

        tk.Label(right, text="Name", **lbl).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
        self.name_var = tk.StringVar()
        tk.Entry(right, textvariable=self.name_var, **ent).grid(row=0, column=1, pady=(10, 2))

        tk.Label(right, text="Phone", **lbl).grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.phone_var = tk.StringVar()
        tk.Entry(right, textvariable=self.phone_var, **ent).grid(row=1, column=1, pady=2)

        tk.Label(right, text="Email", **lbl).grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.email_var = tk.StringVar()
        tk.Entry(right, textvariable=self.email_var, **ent).grid(row=2, column=1, pady=2)

        tk.Label(right, text="Address", **lbl).grid(row=3, column=0, sticky="nw", padx=10, pady=2)
        self.addr_text = tk.Text(right, width=28, height=4, bg=self.colors["input_bg"],
                                 relief="flat", font=("Helvetica", 10))
        self.addr_text.grid(row=3, column=1, pady=2)

        btn_frame = tk.Frame(right, bg=self.colors["frame"])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=12)

        def mk(txt, cmd):
            tk.Button(btn_frame, text=txt, width=10, bg=self.colors["accent"], fg="white",
                      activebackground=self.colors["accent_dark"], borderwidth=0,
                      command=cmd).pack(side="left", padx=4)

        mk("Add", self.add_contact)
        mk("Update", self.update_contact)
        mk("Delete", self.delete_contact)
        mk("Clear", self.clear_fields)

        self.refresh_list()

    def list_visible_contacts(self):
        q = self.search_var.get().lower().strip()
        return sorted([(cid, info) for cid, info in self.data.items()
                       if q in info["name"].lower() or q in info["phone"].lower()],
                      key=lambda x: x[1]["name"].lower())

    def refresh_list(self, *_):
        self.listbox.delete(0, tk.END)
        for _cid, info in self.list_visible_contacts():
            self.listbox.insert(tk.END, f"{info['name']} — {info['phone']}")

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.addr_text.delete(1.0, tk.END)
        self.listbox.selection_clear(0, tk.END)
        self.current_id = None

    def on_select(self, _):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        cid, info = self.list_visible_contacts()[index]
        self.current_id = cid
        self.name_var.set(info["name"])
        self.phone_var.set(info["phone"])
        self.email_var.set(info["email"])
        self.addr_text.delete(1.0, tk.END)
        self.addr_text.insert(tk.END, info["address"])

    def validate(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Please enter the contact's name.")
            return
        if not phone:
            messagebox.showwarning("Missing phone", "Please enter the contact's phone number.")
            return
        return {"name": name, "phone": phone,
                "email": self.email_var.get().strip(),
                "address": self.addr_text.get(1.0, tk.END).strip()}

    def add_contact(self):
        info = self.validate()
        if not info:
            return
        self.data[str(uuid4())] = info
        save_contacts(self.data)
        self.refresh_list(); self.clear_fields()

    def update_contact(self):
        if not getattr(self, "current_id", None):
            messagebox.showinfo("Select contact", "Please select a contact to update.")
            return
        info = self.validate()
        if not info:
            return
        self.data[self.current_id] = info
        save_contacts(self.data)
        self.refresh_list(); self.clear_fields()

    def delete_contact(self):
        if not getattr(self, "current_id", None):
            messagebox.showinfo("Select contact", "Please select a contact to delete.")
            return
        if messagebox.askyesno("Confirm delete", "Delete this contact?"):
            self.data.pop(self.current_id, None)
            save_contacts(self.data)
            self.refresh_list(); self.clear_fields()

if __name__ == "__main__":
    ContactBookApp().mainloop()
