import json
import tkinter as tk
from tkinter import filedialog


class SettingsView:
    def __init__(self, master):
        self.master = master
        self.master.title("Ustawienia")
        self.master.geometry("300x200")
        self.master.resizable(False, False)
        self.file_path = None

        # Pasek nawigacyjny
        self.navbar = tk.Frame(self.master, bg='gray', height=50)
        self.navbar.pack(side=tk.TOP, fill=tk.X)

        self.button1 = tk.Button(self.navbar, text="Import", width=10, command=self.call_method1)
        self.button1.pack(side=tk.LEFT, padx=10)
        self.button1.bind("<Enter>", lambda event: self.button1.config(bg="lightblue"))
        self.button1.bind("<Leave>", lambda event: self.button1.config(bg="#f0f0f0"))

        self.button2 = tk.Button(self.navbar, text="Export", width=10, command=self.call_method2)
        self.button2.pack(side=tk.LEFT, padx=10)
        self.button2.bind("<Enter>", lambda event: self.button2.config(bg="lightblue"))
        self.button2.bind("<Leave>", lambda event: self.button2.config(bg="#f0f0f0"))

        self.button3 = tk.Button(self.navbar, text="Save", width=10, command=self.call_method3)
        self.button3.pack(side=tk.RIGHT, padx=10)
        self.button3.bind("<Enter>", lambda event: self.button3.config(bg="lightblue"))
        self.button3.bind("<Leave>", lambda event: self.button3.config(bg="#f0f0f0"))

        # label setup
        self.text = ""
        self.label = tk.Label(self.master, bg='gray', text=self.text, font=("Helvetica", 8))
        self.label.pack(side=tk.BOTTOM, fill=tk.X)

        self.l_div = tk.Frame(self.master)
        self.l_div.pack(side=tk.LEFT, fill=tk.X)

        self.r_div = tk.Frame(self.master)
        self.r_div.pack(side=tk.RIGHT, fill=tk.X)

        l_entry_frame = [tk.Frame(self.l_div) for _ in range(5)]
        r_entry_frame = [tk.Frame(self.r_div) for _ in range(5)]

        # ratio
        l_entry_frame[0].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[0], text="aspect ratio:").pack(side=tk.LEFT, padx=5)

        r_entry_frame[0].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[0], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT)
        tk.Label(r_entry_frame[0], text="between").pack(side=tk.LEFT, padx=5)
        tk.Entry(r_entry_frame[0], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT, padx=(0, 80))

        # w
        l_entry_frame[1].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[1], text="w:").pack(side=tk.LEFT, padx=5)

        r_entry_frame[1].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[1], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT)
        tk.Label(r_entry_frame[1], text="between").pack(side=tk.LEFT, padx=5)
        tk.Entry(r_entry_frame[1], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT)

        # h
        l_entry_frame[2].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[2], text="h:").pack(side=tk.LEFT, padx=5)

        r_entry_frame[2].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[2], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT)
        tk.Label(r_entry_frame[2], text="between").pack(side=tk.LEFT, padx=5)
        tk.Entry(r_entry_frame[2], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT)

        # thresh
        l_entry_frame[3].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[3], text="thresh:").pack(side=tk.LEFT, padx=5)
        r_entry_frame[3].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[3], textvariable=tk.IntVar(), width=5).pack(side=tk.LEFT)

    def call_read(self):
        pass

    def call_method1(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            data = json.load(self.file_path)
            if data:
                self.label.config(text=data.Name)
            else:
                self.label.config(text="Uszkodzony JSON.")
        else:
            self.label.config(text="Proszę wybrać plik JSON.")

    def call_method2(self):
        pass

    def call_method3(self):
        pass
