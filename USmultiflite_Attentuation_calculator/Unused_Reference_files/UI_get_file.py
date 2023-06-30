from tkinter import *
from tkinter import filedialog

root = Tk()

root.withdraw()
filename = filedialog.askopenfilename(title="Open .txt file for SHORTER LENGTH L2 or WATER-ONLY L2")
print(filename)