mport customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Advanced Password Generator")
root.geometry("650x700")

LETTERS = string.ascii_letters
NUMBERS = string.digits
SYMBOLS = string.punctuation

AMBIGUOUS = "0O1lI"

history = []

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 3:
        return "Weak", 0.33

    elif score <= 5:
        return "Medium", 0.66

    else:
        return "Strong", 1.0


def update_length(value):
    length_label.configure(text=f"Password Length : {int(value)}")

def update_history(password):

    history.insert(0, password)

    if len(history) > 5:
        history.pop()

    history_box.configure(state="normal")
    history_box.delete("1.0", tk.END)

    for item in history:
        history_box.insert(tk.END, item + "\n")

    history_box.configure(state="disabled")

def generate_password():

    length = int(length_slider.get())

    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()
    exclude = ambiguous_var.get()

    if not (use_letters or use_numbers or use_symbols):
        messagebox.showerror(
            "Error",
            "Please select at least one character type."
        )
        return

    pools = []

    if use_letters:
        chars = LETTERS
        if exclude:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        pools.append(chars)

    if use_numbers:
        chars = NUMBERS
        if exclude:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        pools.append(chars)

    if use_symbols:
        chars = SYMBOLS
        pools.append(chars)

    all_characters = ''.join(pools)

    if len(all_characters) == 0:
        messagebox.showerror(
            "Error",
            "No valid characters available."
        )
        return

    password = []

    for pool in pools:
        password.append(secrets.choice(pool))

    while len(password) < length:
        password.append(secrets.choice(all_characters))

    for i in range(len(password) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    password = ''.join(password)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    pyperclip.copy(password)

    strength, value = check_strength(password)

    strength_label.configure(text=f"Strength : {strength}")
    strength_bar.set(value)

    update_history(password)

    messagebox.showinfo(
        "Success",
        "Password copied to clipboard!"
    )

title = ctk.CTkLabel(
    root,
    text="Advanced Password Generator",
    font=("Arial", 24, "bold")
)
title.pack(pady=15)

length_label = ctk.CTkLabel(
    root,
    text="Password Length : 12",
    font=("Arial", 15)
)
length_label.pack()

length_slider = ctk.CTkSlider(
    root,
    from_=6,
    to=32,
    number_of_steps=26,
    command=update_length
)
length_slider.pack(pady=10)
length_slider.set(12)

letters_var = ctk.BooleanVar(value=True)
numbers_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=True)
ambiguous_var = ctk.BooleanVar(value=False)

frame = ctk.CTkFrame(root)
frame.pack(pady=10)

ctk.CTkCheckBox(
    frame,
    text="Letters",
    variable=letters_var
).grid(row=0, column=0, padx=10, pady=5)

ctk.CTkCheckBox(
    frame,
    text="Numbers",
    variable=numbers_var
).grid(row=0, column=1, padx=10, pady=5)

ctk.CTkCheckBox(
    frame,
    text="Symbols",
    variable=symbols_var
).grid(row=0, column=2, padx=10, pady=5)

ctk.CTkCheckBox(
    frame,
    text="Exclude Ambiguous Characters",
    variable=ambiguous_var
).grid(row=1, column=0, columnspan=3, pady=5)

password_entry = ctk.CTkEntry(
    root,
    width=420,
    height=40,
    font=("Arial", 16),
    justify="center"
)
password_entry.pack(pady=15)

generate_button = ctk.CTkButton(
    root,
    text="Generate Password",
    width=220,
    height=40,
    font=("Arial", 16, "bold"),
    command=generate_password
)
generate_button.pack(pady=10)

strength_label = ctk.CTkLabel(
    root,
    text="Strength : ",
    font=("Arial", 15, "bold")
)
strength_label.pack(pady=(15, 5))

strength_bar = ctk.CTkProgressBar(
    root,
    width=300
)
strength_bar.pack()
strength_bar.set(0)

clipboard_label = ctk.CTkLabel(
    root,
    text="Generated passwords are copied to the clipboard automatically.",
    font=("Arial", 12)
)
clipboard_label.pack(pady=10)

history_title = ctk.CTkLabel(
    root,
    text="Last 5 Generated Passwords",
    font=("Arial", 16, "bold")
)
history_title.pack(pady=(20, 5))

history_box = tk.Text(
    root,
    width=45,
    height=5,
    font=("Consolas", 12)
)
history_box.pack()

history_box.configure(state="disabled")

update_length(length_slider.get())
root.mainloop()