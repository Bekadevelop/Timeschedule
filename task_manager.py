# import tkinter as tk
# from tkinter import ttk  # For using the combobox
# from tkinter import messagebox
# from tkcalendar import Calendar

# # Main window
# root = tk.Tk()
# root.title("Простой планировщик задач")
# root.geometry("500x400")
# root.configure(bg="#f0f8ff")

# # Function to add task
# def add_task():
#     task = task_entry.get()
#     date = calendar.get_date()
#     priority = priority_var.get()

#     if task.strip() == "":
#         messagebox.showwarning("Ошибка", "Введите задачу!")
#     else:
#         task_list.insert(tk.END, f"{date} - {task} ({priority})")
#         task_entry.delete(0, tk.END)

# # Function to set rating
# def set_rating(rating):
#     global selected_rating
#     selected_rating = rating
#     # Update color of smileys
#     for i in range(5):
#         if i < rating:
#             smileys[i].config(bg="yellow")
#         else:
#             smileys[i].config(bg="lightgray")

# # Widgets
# title_label = tk.Label(root, text="Мой планировщик задач", font=("Helvetica", 16, 'bold'), bg="#4682b4", fg="white")
# title_label.pack(pady=10, fill=tk.X)

# task_frame = tk.Frame(root, bg="#f0f8ff")
# task_frame.pack(pady=20)

# task_label = tk.Label(task_frame, text="Введите задачу:", bg="#f0f8ff", font=("Arial", 12, 'italic'), fg="#4682b4")
# task_label.grid(row=0, column=0, padx=5)

# task_entry = tk.Entry(task_frame, width=30, font=("Arial", 12), bd=2, relief="solid", highlightthickness=2)
# task_entry.grid(row=0, column=1, padx=5)

# priority_label = tk.Label(task_frame, text="Приоритет:", bg="#f0f8ff", font=("Arial", 12), fg="#4682b4")
# priority_label.grid(row=1, column=0, padx=5, pady=5)

# priority_var = tk.StringVar(value="Низкий")
# priority_menu = ttk.Combobox(task_frame, textvariable=priority_var, values=["Низкий", "Средний", "Высокий"], state="readonly", font=("Arial", 12))
# priority_menu.grid(row=1, column=1, padx=5, pady=5)

# calendar = Calendar(root, selectmode="day", date_pattern="dd/mm/yyyy", background="#4682b4", foreground="white", font=("Arial", 12), selectbackground="lightblue")
# calendar.pack(pady=10)

# # Rating scale (smileys)
# rating_frame = tk.Frame(root, bg="#f0f8ff")
# rating_frame.pack(pady=10)

# smiley_texts = ["😡", "😟", "😐", "🙂", "😊"]  # Ratings from 1 to 5
# smileys = []

# selected_rating = 0  # Initial rating

# for i in range(5):
#     smiley_button = tk.Button(rating_frame, text=smiley_texts[i], font=("Arial", 18), bg="lightgray", command=lambda i=i: set_rating(i + 1))
#     smiley_button.grid(row=0, column=i, padx=5)
#     smileys.append(smiley_button)

# add_task_button = tk.Button(root, text="Добавить задачу", command=add_task, bg="#4682b4", fg="white", font=("Arial", 12), relief="raised", bd=3)
# add_task_button.pack(pady=10)

# task_list = tk.Listbox(root, width=60, height=10, font=("Arial", 12), bd=2, relief="sunken", highlightthickness=1, selectbackground="#e0e0e0", selectmode=tk.SINGLE)
# task_list.pack(pady=10)

# # Start the application
# root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

# Main window
root = tk.Tk()
root.title("Простой планировщик задач")
root.geometry("500x400")
root.configure(bg="#f0f8ff")

# Function to add task
def add_task():
    task = task_entry.get()
    date = calendar.get_date()

    if task.strip() == "":
        messagebox.showwarning("Ошибка", "Введите задачу!")
    else:
        task_list.insert(tk.END, f"{date} - {task} (Приоритет: {priority})")
        task_entry.delete(0, tk.END)

# Function to set rating
def set_rating(rating):
    global priority
    priority = ["Низкий", "Средний", "Высокий", "Очень высокий", "Максимальный"][rating - 1]  # Set the priority based on rating
    # Update color of smileys
    for i in range(5):
        if i < rating:
            smileys[i].config(bg="yellow")
        else:
            smileys[i].config(bg="lightgray")

# Function to show tooltip
def show_tooltip(event, rating):
    tooltip_label.config(text=f"Приоритет: {rating}")

def hide_tooltip(event):
    tooltip_label.config(text="")

# Widgets
title_label = tk.Label(root, text="Мой планировщик задач", font=("Helvetica", 16, 'bold'), bg="#4682b4", fg="white")
title_label.pack(pady=10, fill=tk.X)

task_frame = tk.Frame(root, bg="#f0f8ff")
task_frame.pack(pady=20)

task_label = tk.Label(task_frame, text="Введите задачу:", bg="#f0f8ff", font=("Arial", 12, 'italic'), fg="#4682b4")
task_label.grid(row=0, column=0, padx=5)

task_entry = tk.Entry(task_frame, width=30, font=("Arial", 12), bd=2, relief="solid", highlightthickness=2)
task_entry.grid(row=0, column=1, padx=5)

calendar = Calendar(root, selectmode="day", date_pattern="dd/mm/yyyy", background="#4682b4", foreground="white", font=("Arial", 12), selectbackground="lightblue")
calendar.pack(pady=10)

# Rating scale (smileys)
rating_frame = tk.Frame(root, bg="#f0f8ff")
rating_frame.pack(pady=10)

# Updated smilies with corresponding priority levels
smiley_texts = ["😡", "😟", "😐", "🙂", "😊"]  # Ratings from 1 to 5
smiley_tooltips = ["Очень низкий", "Низкий", "Средний", "Высокий", "Максимальный"]  # Corresponding tooltip text for priority
smileys = []

priority = "Низкий"  # Initial priority

for i in range(5):
    smiley_button = tk.Button(rating_frame, text=smiley_texts[i], font=("Arial", 18), bg="lightgray", command=lambda i=i: set_rating(i + 1))
    smiley_button.grid(row=0, column=i, padx=5)
    smileys.append(smiley_button)
    
    # Bind hover events to show the tooltip with priority
    smiley_button.bind("<Enter>", lambda event, i=i: show_tooltip(event, smiley_tooltips[i]))
    smiley_button.bind("<Leave>", hide_tooltip)

# Tooltip label
tooltip_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f8ff", fg="black")
tooltip_label.pack(pady=5)

add_task_button = tk.Button(root, text="Добавить задачу", command=add_task, bg="#4682b4", fg="white", font=("Arial", 12), relief="raised", bd=3)
add_task_button.pack(pady=10)

task_list = tk.Listbox(root, width=60, height=10, font=("Arial", 12), bd=2, relief="sunken", highlightthickness=1, selectbackground="#e0e0e0", selectmode=tk.SINGLE)
task_list.pack(pady=10)

# Start the application
root.mainloop()
