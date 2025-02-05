import tkinter as tk
from tkinter import ttk, Label
from PIL import Image, ImageTk

# Translation dictionary
translations = {
    "apple": {"Spanish": "manzana", "French": "pomme", "German": "Apfel", "Italian": "mela", "Japanese": "りんご", "Korean": "사과"},
    "banana": {"Spanish": "plátano", "French": "banane", "German": "Banane", "Italian": "banana", "Japanese": "バナナ", "Korean": "バナナ"},
    "beans": {"Spanish": "frijoles", "French": "haricots", "German": "Bohnen", "Italian": "fagioli", "Japanese": "豆", "Korean": "콩"},
    "steak": {"Spanish": "bistec", "French": "steak", "German": "Steak", "Italian": "bistecca", "Japanese": "ステーキ", "Korean": "ステーキ"}
}

# Center
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("Food Translator")
root.geometry("900x600")
center_window(root, 900, 600)

# Load pics
food_items = ["apple", "banana", "beans", "steak"]
images = {}

for item in food_items:
    img = Image.open(f"{item}.jpeg")
    img = img.resize((100, 100))  # Resize the image
    images[item] = ImageTk.PhotoImage(img)

# Update the curr translation
def translate_food(food, language):
    translation_label.config(text=f"{food.capitalize()} in {language}: {translations[food][language]}")

# Main Frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill=tk.BOTH)

# Food Pictures Frame
food_frame = ttk.Frame(main_frame)
food_frame.pack(pady=20)

# Display food images
food_labels = {}
for i, item in enumerate(food_items):
    label = Label(food_frame, image=images[item], text=item, compound="top", font=("Arial", 12), bg="light blue")
    label.grid(row=0, column=i, padx=40, pady=10)  # More space between language button s
    label.bind("<ButtonPress-1>", lambda e, f=item: start_drag(e, f))
    food_labels[item] = label

# Dragging variables
dragging = False
current_item = None
floating_label = None

def start_drag(event, food):
    global dragging, current_item, floating_label
    dragging = True
    current_item = food

    if floating_label:
        floating_label.destroy()
    
    floating_label = Label(root, image=images[food], text=food, compound="top", font=("Arial", 12), bg="light blue")
    floating_label.place(x=event.x_root, y=event.y_root, anchor="center")
    root.bind("<B1-Motion>", move_floating_label)
    root.bind("<ButtonRelease-1>", stop_drag)

def move_floating_label(event):
    if dragging and floating_label:
        floating_label.place(x=event.x_root, y=event.y_root, anchor="center")

def stop_drag(event):
    global dragging, current_item, floating_label
    if dragging:
        dragging = False

        # Check for image position overlap with language buttons
        closest_button = None
        min_distance = float("inf")
        fx, fy = event.x_root, event.y_root

        for lang, btn in language_buttons.items():
            bx, by = btn.winfo_rootx() + btn.winfo_width() // 2, btn.winfo_rooty() + btn.winfo_height() // 2
            distance = ((fx - bx) ** 2 + (fy - by) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_button = lang

        if closest_button:
            translate_food(current_item, closest_button)

        floating_label.destroy()
        floating_label = None
        root.unbind("<B1-Motion>")
        root.unbind("<ButtonRelease-1>")

# Language Buttons Frame
language_frame = ttk.Frame(main_frame)
language_frame.pack(pady=50)

# Language buttons (prob will add more)
languages = ["Spanish", "French", "German", "Italian", "Japanese", "Korean"]
language_buttons = {}

for i, lang in enumerate(languages):
    btn = ttk.Button(language_frame, text=lang, style="TButton")
    btn.grid(row=0, column=i, padx=50, pady=20)  # Increased spacing further
    language_buttons[lang] = btn

# Translation display
translation_label = Label(main_frame, text="Select a food and a language", font=("Arial", 16), bg="light blue")
translation_label.pack(pady=20)

# Design
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.map("TButton", background=[("active", "light blue")])

root.configure(bg="light blue")
root.mainloop()
