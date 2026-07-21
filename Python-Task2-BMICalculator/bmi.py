import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
DB_NAME = "bmi_records.db"

def create_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            date TEXT
        )
        """)

        conn.commit()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
create_database()

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "blue"

    elif bmi < 25:
        return "Normal", "green"

    elif bmi < 30:
        return "Overweight", "orange"

    else:
        return "Obese", "red"
    
def save_record(username, weight, height, bmi, category):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO bmi_records
        (username, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def calculate_bmi():

    username = entry_name.get().strip()

    if username == "":
        messagebox.showerror("Error", "Enter username")
        return

    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if weight <= 0 or height <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Weight and Height must be positive numbers."
        )
        return

    bmi = weight / (height ** 2)

    category, color = classify_bmi(bmi)

    result_label.config(
        text=f"BMI : {bmi:.2f}\nCategory : {category}",
        fg=color
    )

    save_record(username, weight, height, bmi, category)

    messagebox.showinfo("Saved", "BMI record saved successfully.")

def show_history():

    username = entry_name.get().strip()

    if username == "":
        messagebox.showerror("Error", "Enter username")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT date,bmi,category
        FROM bmi_records
        WHERE username=?
        ORDER BY id
        """, (username,))

        records = cursor.fetchall()

        conn.close()

        history_window = tk.Toplevel(root)
        history_window.title("History")

        text = tk.Text(history_window, width=60, height=20)
        text.pack()

        if len(records) == 0:
            text.insert(tk.END, "No records found.")
        else:
            for row in records:
                text.insert(
                    tk.END,
                    f"{row[0]}    BMI:{row[1]:.2f}    {row[2]}\n"
                )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def show_graph():

    username = entry_name.get().strip()

    if username == "":
        messagebox.showerror("Error", "Enter username")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT date,bmi
        FROM bmi_records
        WHERE username=?
        ORDER BY id
        """, (username,))

        records = cursor.fetchall()

        conn.close()

        if len(records) == 0:
            messagebox.showinfo("Info", "No records found.")
            return

        dates = [r[0] for r in records]
        bmi_values = [r[1] for r in records]

        plt.figure(figsize=(8,4))
        plt.plot(dates, bmi_values, marker='o')
        plt.title(f"{username}'s BMI Trend")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("450x450")

title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

tk.Label(root, text="User Name").pack()

entry_name = tk.Entry(root, width=30)
entry_name.pack()

tk.Label(root, text="Weight (kg)").pack()

entry_weight = tk.Entry(root, width=30)
entry_weight.pack()

tk.Label(root, text="Height (m)").pack()

entry_height = tk.Entry(root, width=30)
entry_height.pack()


tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="lightblue",
    width=20
).pack(pady=10)


tk.Button(
    root,
    text="View History",
    command=show_history,
    width=20
).pack(pady=5)


tk.Button(
    root,
    text="Show BMI Graph",
    command=show_graph,
    width=20
).pack(pady=5)


result_label = tk.Label(
    root,
    text="",
    font=("Arial", 16, "bold")
)

result_label.pack(pady=20)


root.mainloop()