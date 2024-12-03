import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import Parser
from node import *
from Parser import *


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            input_field.config(state='normal')
            input_field.delete(1.0, tk.END)  # Clear the Text widget first
            input_field.insert(tk.END, f.read())  # Insert the new data
            input_field.config(state='disabled')


def generate_canvas():
    global list_of_tokens
    input_content = input_field.get("1.0", "end")
    graph_area.delete("all")
    Parser.list_of_tokens = split_input(input_content)
    print(Parser.list_of_tokens)
    root_node = program()
    error = contains_errors(root_node)
    # draw_canvas(root_node, 100, 50, 100, 100)
    if error:
        display_string(error)
        print(error)
    else:
        draw_canvas(root_node, 100, 50, 100, 100)


def display_string(text):
    graph_area.create_text(300, 20, text=text, anchor="center" , fill="red", font=("Helvetica", 12))


def split_input(input_content):
    return [tuple(item.strip() for item in line.split(','))
            for line in input_content.split('\n') if line.strip()]


def draw_canvas(node: Node, x: int, y: int, spacing_x: int, spacing_y: int) -> int:
    # Accumulate x for correct horizontal positioning
    child_x = x
    child_y = y + spacing_y
    for child in node.children:
        graph_area.create_line(x, y - 5, child_x, child_y - 5, fill="white")
        child_x = draw_canvas(child, child_x, child_y, spacing_x, spacing_y) + spacing_x
    if (len(node.children) >= 1):
        child_x -= spacing_x

    if node.next:
        next_x = child_x + spacing_x
        next_y = y
        graph_area.create_line(x + 20, y, next_x - 20, next_y, fill="white")
        child_x = draw_canvas(node.next, next_x, next_y, spacing_x, spacing_y)

    # Differentiate square and oval with background and border colors
    if node.is_square:
        graph_area.create_rectangle(
            x - 30, y - 30, x + 30, y + 30, fill="white", outline="red"
        )
    else:
        graph_area.create_oval(
            x - 40, y - 20, x + 40, y + 20, fill="white", outline="blue"
        )

    graph_area.create_text(x, y, text=node.data, anchor="center")
    return child_x


root = tk.Tk()
root.title("Tiny Language Parser")

# Apply the dark mode theme
root.configure(bg='#2c2c2c')
style = ttk.Style(root)
style.theme_use('clam')
style.configure('TLabel', background='#2c2c2c', foreground='white')
style.configure('TButton', background='#4c4c4c', foreground='white', borderwidth=0)

# Create the input text field
# Create a Text widget for multiline input
input_field = tk.Text(root, wrap="word", font=('Courier', 12),
                      bg='#2c2c2c', fg='white', insertbackground='white',
                      width=30,
                      highlightbackground='white', highlightcolor='white', highlightthickness=2)
input_field.grid(row=0, column=0, padx=10, pady=10, sticky='ns')
input_field.config(state='disabled')

# Create the graph area
graph_area = tk.Canvas(root, bg='#2c2c2c')
graph_area.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')

# Create the "Browse" button
browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# Create the "Draw" button
draw_button = ttk.Button(root, text="Draw", width=40, command=generate_canvas)
draw_button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

# Create the logo image
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((150, 77), resample=Image.BICUBIC)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = ttk.Label(root, image=logo_photo, background='#2c2c2c')
logo_label.grid(row=1, column=3, padx=10, pady=10, sticky='nsew')

# Make the labels and buttons resize with the window
root.rowconfigure(0, weight=1)

# root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.mainloop()
