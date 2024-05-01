import tkinter as tk
from tkinter import ttk

def add_task():
    task = task_entry.get()
    if task:
        task_id = task_tree.insert("", tk.END, text=task, values=("☐",))
        task_entry.delete(0, tk.END)

def check_task(event):
    item = task_tree.selection()[0]
    checked = task_tree.item(item, "values")[0]
    if checked == "☐":
        task_tree.item(item, values=("✔",))
    else:
        task_tree.item(item, values=("☐",))

def delete_task():
    selected_item = task_tree.selection()
    for item in selected_item:
        task_tree.delete(item)

root = tk.Tk()
root.title("Список задач:")
root.geometry("400x550+800+300")
root.configure(bg="lightblue")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="gray", foreground="white", font=("Arial", 12))
style.configure("TButton", padding=10, font=("Arial", 10))

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False) # здесь мы ставим полоску прокрутки expand = False по умолчанию

text1 = ttk.Label(root, text="Введите вашу задачу:", style="TLabel", font="none 12 bold")
text1.pack(pady=20, padx=5)

task_entry = ttk.Entry(root, width=30)
task_entry.pack(pady=20)

add_task_button = ttk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.pack(pady=10)

text2 = ttk.Label(root, text="Список задач:", style="TLabel", font="none 12 bold")
text2.pack(pady=20)

task_tree = ttk.Treeview(root, columns=("Готово",), displaycolumns=("Готово",))
task_tree.heading("#0", text="Задача")
task_tree.heading("Готово", text="Готово")
task_tree.column("#0", width=280)
task_tree.column("Готово", width=50, anchor='center')
task_tree.pack()
task_tree.bind("<Double-1>", check_task)

task_tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_tree.yview)

delete_button = ttk.Button(root, text="Удалить задачу", command=delete_task)
delete_button.pack(pady=10)

root.mainloop()