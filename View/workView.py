import tkinter as tk

from PIL import ImageTk

from Model.ImgProcessing import ImgProcessing


class WorkView:
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

        self.button1 = tk.Button(self.navbar, text="Open", width=10, command=self.call_method1)
        self.button1.pack(side=tk.LEFT, padx=10)
        self.button1.bind("<Enter>", lambda event: self.button1.config(bg="lightblue"))
        self.button1.bind("<Leave>", lambda event: self.button1.config(bg="#f0f0f0"))

        self.button2 = tk.Button(self.navbar, text="Read Code", width=10, command=self.call_method2)
        self.button2.pack(side=tk.LEFT, padx=10)
        self.button2.bind("<Enter>", lambda event: self.button2.config(bg="lightblue"))
        self.button2.bind("<Leave>", lambda event: self.button2.config(bg="#f0f0f0"))

        self.button3 = tk.Button(self.navbar, text="Copy&Save", width=10, command=self.call_method3)
        self.button3.pack(side=tk.LEFT, padx=10)
        self.button3.bind("<Enter>", lambda event: self.button3.config(bg="lightblue"))
        self.button3.bind("<Leave>", lambda event: self.button3.config(bg="#f0f0f0"))

        self.button4 = tk.Button(self.navbar, text="Settings", width=10, command=self.call_method4)
        self.button4.pack(side=tk.RIGHT, padx=10)
        self.button4.bind("<Enter>", lambda event: self.button4.config(bg="lightblue"))
        self.button4.bind("<Leave>", lambda event: self.button4.config(bg="#f0f0f0"))

        # canvas setup
        self.canvas = tk.Canvas(self.master, width=600, height=400)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH)
        self.tk_image = None

        # label setup
        self.text = ""
        self.label = tk.Label(self.master, bg='gray', text=self.text, font=("Helvetica", 14))
        self.label.pack(side=tk.BOTTOM, fill=tk.X)

    def call_method1(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        tk_image = self.img.openTk(w, h)
        if tk_image:
            self.tk_image = tk_image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def call_method2(self):
        tk_image, text = self.img.OCR()
        tk_image = ImageTk.PhotoImage(tk_image)
        self.label.config(text=text)
        if tk_image is not None:
            self.tk_image = tk_image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def call_method3(self):
        self.label.config(text=self.img.saveTk())

    def call_method4(self):
        pass
