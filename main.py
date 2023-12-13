from View.mainView import MainView
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = MainView(root)
    root.geometry("600x450")
    root.mainloop()
