import tkinter as tk
from Model.ImgProcessing import ImgProcessing

class MainView:
    def __init__(self, master):
        # main setup
        self.master = master
        self.master.title("Aplikacja do przetwarzania zdjęć")
        self.master.geometry("600x450")
        self.master.resizable(False, False)

        # class init
        self.img = ImgProcessing()

        # Pasek nawigacyjny
        self.navbar = tk.Frame(self.master, bg='gray', height=50)
        self.navbar.pack(side=tk.TOP, fill=tk.X)

        self.button1 = tk.Button(self.navbar, text="Otwórz", width=10, command=self.call_method1)
        self.button1.pack(side=tk.LEFT, padx=10)
        self.button1.bind("<Enter>", lambda event: self.button1.config(bg="lightblue"))
        self.button1.bind("<Leave>", lambda event: self.button1.config(bg="lightgray"))

        self.button2 = tk.Button(self.navbar, text="Zapisz", width=10, command=self.call_method2)
        self.button2.pack(side=tk.LEFT, padx=10)
        self.button2.bind("<Enter>", lambda event: self.button2.config(bg="lightblue"))
        self.button2.bind("<Leave>", lambda event: self.button2.config(bg="lightgray"))

        # canvas setup
        self.canvas = tk.Canvas(self.master, width=600, height=450)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.tk_image = None

    def call_method1(self):
        w = self.canvas.winfo_width() - 2
        h = self.canvas.winfo_height() - 2
        tk_image = self.img.openTk(w, h)
        if tk_image:
            self.tk_image = tk_image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def call_method2(self):
        self.img.saveTk()
