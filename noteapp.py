import tkinter as tk
import os
from pathlib import Path
from tkinter import simpledialog, ttk
from PIL import Image, ImageTk  # Import PIL for image handling

# Main window
root = tk.Tk()

# Window properties
root.title('note app')
root.geometry('400x300')
root.resizable(False, False)

# Canvas setup
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create lines
# Big line
canvas.create_line(70, 0, 70, 300)
# Small line
canvas.create_line(0, 25, 400, 25)

########################################################################################

# Set directory
directory = Path(os.path.dirname(os.path.abspath(__file__)))

# List all .txt files in the directory
txt_files = [file.name for file in directory.iterdir() if file.is_file() and file.name.endswith('.txt')]

# Create a frame for the Listbox and Scrollbar
frame = tk.Frame(root)
frame.place(x=2.5, y=30, width=62.5, height=265)

# Create a Listbox to display the .txt files
listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a Scrollbar to the Listbox
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Listbox to work with the Scrollbar
listbox.config(yscrollcommand=scrollbar.set)

# Populate the Listbox with .txt files
for txt_file in txt_files:
    listbox.insert(tk.END, txt_file)

########################################################################################

# Define function to write to file
def create_file():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    note_name = simpledialog.askstring("Create note", "Enter filename:")

    # Construct the full path for note.txt
    file_path = os.path.join(current_dir, note_name + ".txt")

    # Create a Text widget for editing the file content
    file_text = tk.Text(root, wrap='word', font=('Arial', 12))
    file_text.pack(fill=tk.BOTH)
    file_text.place(x=70.5, y=26, width=328, height=272.5, anchor='nw')
    
    # If the file exists, load its content into the Text widget
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
            file_text.insert(tk.END, file_content)
    
    # Function to save the content of the Text widget
    def save_content():
        # Get the content of the Text widget
        text_content = file_text.get("1.0", tk.END).strip()  # Get all text from line 1, character 0 to the end
        with open(file_path, 'w') as file:
            file.write(text_content)  # Save the content to the file

    # Add a Save button to save the content
    save_button = ttk.Button(root, text="Save", command = save_content)
    save_button.place(x = 350, y = 11, anchor='center')

########################################################################################

def save_file():
    # Get the selected file name from the Listbox
    selected_file = listbox.get(listbox.curselection())
    
    # Construct the full path for the selected file
    file_path = os.path.join(directory, selected_file)
    
    # Write to the file
    with open(file_path, 'w') as file:
        file.write('idk')

########################################################################################

def on_item_selected(event):
    # Get the selected item's index
    selected_index = listbox.curselection()
    if selected_index:  # Check if an item is selected
        # Get the selected item's text
        selected_file = listbox.get(selected_index[0])
        file_path = os.path.join(directory, selected_file)

        # Create a Text widget for editing the file content
        file_text = tk.Text(root, wrap='word', font=('Arial', 12))
        file_text.pack(fill=tk.BOTH)
        file_text.place(x=70.5, y=26, width=328, height=272.5, anchor='nw')

        # Load the content of the selected file into the Text widget
        with open(file_path, 'r') as file:
            file_content = file.read()
            file_text.insert(tk.END, file_content)

        # Function to save the content of the Text widget
        def save_content():
            # Get the content of the Text widget
            text_content = file_text.get("1.0", tk.END).strip()  # Get all text from line 1, character 0 to the end
            with open(file_path, 'w') as file:
                file.write(text_content)  # Save the content to the file

        # Add a Save button to save the content
        save_button = ttk.Button(root, text="Save", command=save_content)
        save_button.place(x=350, y=11, anchor='center')

# Bind the Listbox selection event to the on_item_selected function
listbox.bind('<<ListboxSelect>>', on_item_selected)

# Create new file button
create_file_button = ttk.Button(root, text='+', width=3, command = create_file)
create_file_button.pack()
create_file_button.place(x=2, y=-3, anchor='nw')

########################################################################################

def refresh_listbox():
    # Clear the current contents of the Listbox
    listbox.delete(0, tk.END)
    
    # Refresh the list of .txt files in the directory
    txt_files = [file.name for file in directory.iterdir() if file.is_file() and file.name.endswith('.txt')]
    
    # Repopulate the Listbox with updated .txt files
    for txt_file in txt_files:
        listbox.insert(tk.END, txt_file)
    
    # Schedule the function to run again after 1000 milliseconds (1 second)
    root.after(1000, refresh_listbox)

# Call the refresh_listbox function to start the periodic refresh
refresh_listbox()

########################################################################################

# Main loop
root.mainloop()