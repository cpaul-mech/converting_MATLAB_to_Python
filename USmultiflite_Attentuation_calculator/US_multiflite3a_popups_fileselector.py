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
import tkinter as tk
from tkinter import filedialog
import os

# Create the root window
root = tk.Tk()
root.geometry("300x200")
root.title("File Selector")

file_type_options = [".txt", ".isf", ".xls"]

# Create the function that will be called when the button is pressed
def show():
    label.config( text = clicked.get() )

clicked = tk.StringVar()

# initial menu text
clicked.set( ".txt" )
  
# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()
  
# Create button, it will change label text
button = Button( root , text = "click Me" , command = show ).pack()
  
# Create Label
label = Label( root , text = " " )
label.pack()
  
# Execute tkinter
root.mainloop()

