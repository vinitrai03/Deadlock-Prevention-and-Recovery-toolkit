# main.py: Main entry point (Runs the GUI)
from gui import DeadlockGUI
from tkinter import *

if __name__ == "__main__":
    root = Tk()
    gui = DeadlockGUI(root)
    root.mainloop()