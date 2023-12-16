from View.workView import WorkView
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = WorkView(root)
    root.geometry("600x450")
    root.mainloop()