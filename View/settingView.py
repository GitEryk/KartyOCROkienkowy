import os
import tkinter as tk
from Model.ImgProcessing import ImgProcessing


class SettingsView:
    def __init__(self, master):
        self.master = master
        self.master.title("Ustawienia")
        self.master.geometry("300x200")
        self.master.resizable(False, False)
        self.file_path = None

        self.ratio1_var = tk.DoubleVar(value=0)
        self.ratio2_var = tk.DoubleVar(value=0)
        self.w1_var = tk.IntVar(value=0)
        self.w2_var = tk.IntVar(value=0)
        self.h1_var = tk.IntVar(value=0)
        self.h2_var = tk.IntVar(value=0)
        self.thresh_var = tk.IntVar(value=0)

        # class init
        self.imgProc = ImgProcessing()

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
        tk.Entry(r_entry_frame[0], textvariable=self.ratio1_var, width=5).pack(side=tk.LEFT)
        tk.Label(r_entry_frame[0], text="between").pack(side=tk.LEFT, padx=5)
        tk.Entry(r_entry_frame[0], textvariable=self.ratio2_var, width=5).pack(side=tk.LEFT, padx=(0, 80))

        # w
        l_entry_frame[1].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[1], text="w:").pack(side=tk.LEFT, padx=5)

        r_entry_frame[1].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[1], textvariable=self.w1_var, width=5).pack(side=tk.LEFT)
        tk.Label(r_entry_frame[1], text="between").pack(side=tk.LEFT, padx=5)
        tk.Entry(r_entry_frame[1], textvariable=self.w2_var, width=5).pack(side=tk.LEFT)

        # h
        l_entry_frame[2].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[2], text="h:").pack(side=tk.LEFT, padx=5)

        r_entry_frame[2].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[2], textvariable=self.h1_var, width=5).pack(side=tk.LEFT)
        tk.Label(r_entry_frame[2], text="between").pack(side=tk.LEFT, padx=5)
        tk.Entry(r_entry_frame[2], textvariable=self.h2_var, width=5).pack(side=tk.LEFT)

        # thresh
        l_entry_frame[3].pack(side=tk.TOP, fill=tk.X)
        tk.Label(l_entry_frame[3], text="thresh:").pack(side=tk.LEFT, padx=5)
        r_entry_frame[3].pack(side=tk.TOP, fill=tk.X)
        tk.Entry(r_entry_frame[3], textvariable=self.thresh_var, width=5).pack(side=tk.LEFT)

        self.call_read()

    def call_read(self):
        file = os.listdir(r"C:\Users\Lenovo\Desktop\pythonProject\Assets")
        dirJson = os.path.join(r"C:\Users\Lenovo\Desktop\pythonProject\Assets", file[0])
        setting, text = self.imgProc.loadSetting(path=dirJson)
        if setting is not None:
            t = f"{text} {setting['name']}"
            self.label.config(text=t)
            self.ratio1_var.set(setting['ratio1'])
            self.ratio2_var.set(setting['ratio2'])
            self.w1_var.set(setting['w1'])
            self.w2_var.set(setting['w2'])
            self.h1_var.set(setting['h1'])
            self.h2_var.set(setting['h2'])
            self.thresh_var.set(setting['thresh'])
        else:
            self.label.config(text=text)

    def call_method1(self):
        setting, text = self.imgProc.loadSetting()
        if setting is not None:
            t = f"{text} {setting['name']}"
            self.label.config(text=t)
            self.ratio1_var.set(setting['ratio1'])
            self.ratio2_var.set(setting['ratio2'])
            self.w1_var.set(setting['w1'])
            self.w2_var.set(setting['w2'])
            self.h1_var.set(setting['h1'])
            self.h2_var.set(setting['h2'])
            self.thresh_var.set(setting['thresh'])
        else:
            self.label.config(text=text)

    def call_method2(self):
        pass

    def call_method3(self):
        pass


if __name__ == "View.settingView":
    root = tk.Tk()
    app = SettingsView(root)
    root.geometry("300x200")
    root.mainloop()
