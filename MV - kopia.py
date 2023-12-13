import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class MainView:
    def __init__(self, master):
        # main setup
        self.master = master
        self.master.title("Aplikacja do przetwarzania zdjęć")
        self.master.geometry("600x450")
        self.master.resizable(False, False)

        # Pasek nawigacyjny
        self.navbar = tk.Frame(self.master, bg='gray', height=50)
        self.navbar.pack(side=tk.TOP, fill=tk.X)

        self.button1 = tk.Button(self.navbar, text="Otwórz", width=10, command=self.method1)
        self.button1.pack(side=tk.LEFT, padx=10)
        self.button1.bind("<Enter>", lambda event: self.button1.config(bg="lightblue"))
        self.button1.bind("<Leave>", lambda event: self.button1.config(bg="lightgray"))

        self.button2 = tk.Button(self.navbar, text="Metoda 2", width=10, command=self.method2)
        self.button2.pack(side=tk.LEFT, padx=10)
        self.button2.bind("<Enter>", lambda event: self.button2.config(bg="lightblue"))
        self.button2.bind("<Leave>", lambda event: self.button2.config(bg="lightgray"))

        self.button3 = tk.Button(self.navbar, text="Metoda 3", width=10, command=self.method3)
        self.button3.pack(side=tk.LEFT, padx=10)
        self.button3.bind("<Enter>", lambda event: self.button3.config(bg="lightblue"))
        self.button3.bind("<Leave>", lambda event: self.button3.config(bg="lightgray"))

        self.button4 = tk.Button(self.navbar, text="Metoda 4", width=10, command=self.method4)
        self.button4.pack(side=tk.LEFT, padx=10)
        self.button4.bind("<Enter>", lambda event: self.button4.config(bg="lightblue"))
        self.button4.bind("<Leave>", lambda event: self.button4.config(bg="lightgray"))

        # canvas setup
        self.canvas = tk.Canvas(self.master, width=600, height=450)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.tk_image = None

    def method1(self):
        print("Wywołano metodę 1")
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((self.canvas.winfo_width()-2, self.canvas.winfo_height()-2))
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    @staticmethod
    def method2():
        print("Wywołano metodę 2")

    @staticmethod
    def method3():
        print("Wywołano metodę 3")

    @staticmethod
    def method4():
        print("Wywołano metodę 4")
