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

file_type_options = [".txt", ".isf", ".xls",".csv"]

def close():
    root.quit()
    


clicked = StringVar()

# initial menu text
clicked.set(file_type_options[3])
  
# Create Dropdown menu
drop = OptionMenu(root , clicked, *file_type_options)
drop.pack(padx=10, pady=10)

# close button
close_button = Button(root,text = "Save and Close",command = close).pack()
  
# Execute tkinter
root.mainloop()
file_type_selected = clicked.get()
print(f'file_type_selected = {clicked.get()}')
root.destroy()

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

col1_name = "Time (s)"
col2_name = "Average (B)"
# Now I need to import the file into a pandas dataframe
if file_type_selected == ".txt":
    df = pd.read_csv(path_string, sep='\t', header=None, names=[col1_name, col2_name])
elif file_type_selected == ".isf":
    df = pd.read_csv(path_string, sep='\t', header=None, names=[col1_name, col2_name])
elif file_type_selected == ".xls":
    df = pd.read_excel(path_string, header=None, names=[col1_name, col2_name])
elif file_type_selected == ".csv":
    df = pd.read_csv(path_string, header=None, names=[col1_name, col2_name])
else:
    print("File type not recognized. Exiting...")
    exit()
root2.destroy()
# The issue is the data starts at line 4 in the txt file, so I need to drop the first 2 rows
df = df.drop([0,1])
print(df.head())
# Now get the second file to compare the two files.
root3 = Tk()
root3.withdraw()
path_string2 = filedialog.askopenfilename(title=f"Open {file_type_selected} file for LONGER LENGTH L2", filetypes=[(f"{file_type_selected} files", f"*{file_type_selected}")])
if path_string2 == "":
    print("No file selected. Exiting...")
    exit()
print(f'path_string2 = {path_string2}')
# we don't actually need to separate the path name from the filename. 

# Now I need to import the file into a pandas dataframe
if file_type_selected == ".txt":
    df2 = pd.read_csv(path_string2, sep='\t', header=None, names=[col1_name, col2_name])
elif file_type_selected == ".isf":
    df2 = pd.read_csv(path_string2, sep='\t', header=None, names=[col1_name, col2_name])
elif file_type_selected == ".xls":
    df2 = pd.read_excel(path_string2, header=None, names=[col1_name, col2_name])
elif file_type_selected == ".csv":
    df2 = pd.read_csv(path_string2, header=None, names=[col1_name, col2_name])
else:
    print("File type not recognized. Exiting...")
    exit()
df2 = df2.drop([0,1])
print(df2.head())
root3.destroy()
print(df2[col1_name])
# Now I need to plot the two files on the same plot after converting them to numpy arrays
time_file1 = df[col1_name].to_numpy()
time_file2 = df2[col1_name].to_numpy()
avg_file1 = df[col2_name].to_numpy()
avg_file2 = df2[col2_name].to_numpy()

import matplotlib.pyplot as plt
plt.plot(time_file1, avg_file1, label="Shorter L2")
plt.plot(time_file2, avg_file2, label="Longer L2")
plt.xlabel("Time (s)")
plt.ylabel("Average (B)")
plt.title("Comparison of Shorter and Longer L2")
plt.legend()
plt.show()

