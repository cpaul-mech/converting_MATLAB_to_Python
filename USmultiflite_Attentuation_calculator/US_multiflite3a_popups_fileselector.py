# This file will imitate the functionality of the file selector in the USmultiflite3a.m file.
"""
This is the code snippet I will convert to python:
[sel,ok] = listdlg('PromptString','Select time-domain file type:','Name','File Type to Open',...
    'SelectionMode','single','ListSize',[150 90],'ListString',['.txt';'.isf';'.xls']);
if ok==0; return; end

repeat=1; firstflag=1;
ii=1; savedt=0;

"""

# Import the necessary modules
from tkinter import *
import numpy as np
import pandas as pd
from tkinter import filedialog
import os

file_type_selected = ""

# Create the root window
root = Tk()
root.geometry("300x200")
root.title("File Type Selector")

# Create a large label above the dropdown menu
login = Label(root, text="Select Time-domain file type:")
login.pack(ipady=5, fill='x')
login.config(font=("Font", 14))

file_type_options = [".txt", ".isf", ".xls"]

def close():
    root.quit()


clicked = StringVar()

# initial menu text
clicked.set(file_type_options[0])
  
# Create Dropdown menu
drop = OptionMenu(root , clicked, *file_type_options)
drop.pack(padx=10, pady=10)

# close button
close_button = Button(root,text = "Save and Close",command = close).pack()
  
# Execute tkinter
root.mainloop()
file_type_selected = clicked.get()
print(f'file_type_selected = {clicked.get()}')

# Now, I need to get the file name
root2 = Tk()
root2.withdraw()
path_string = filedialog.askopenfilename(title=f"Open {file_type_selected} file for SHORTER LENGTH L2 or WATER-ONLY L2", filetypes=[(f"{file_type_selected} files", f"*{file_type_selected}")])
if path_string == "":
    print("No file selected. Exiting...")
    exit()
print(f'path_string = {path_string}')
# now separate the filename from the end of the path after the last slash
# and the file extension
file_name = os.path.basename(path_string)
print(f'file_name = {file_name}')

# Now I need to import the file into a pandas dataframe
if file_type_selected == ".txt":
    df = pd.read_csv(path_string, sep='\t', header=None, names=['time', 'amplitude'])
elif file_type_selected == ".isf":
    df = pd.read_csv(path_string, sep='\t', header=None, names=['time', 'amplitude'])
elif file_type_selected == ".xls":
    df = pd.read_excel(path_string, header=None, names=['time', 'amplitude'])
else:
    print("File type not recognized. Exiting...")
    exit()

print(df.head())

