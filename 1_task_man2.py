import tkinter as tk
from tkinter import ttk, messagebox
import json

# Константы
UNCHECKED = "☐"
CHECKED = "✔"
MAX_TASKS = 50

# Функции
def add_task():
    """Добавление новой задачи в список."""
    if len(task_tree.get_children()) >= MAX_TASKS:
        messagebox.showerror("Ошибка", "Превышено максимальное количество задач!")
        return
    task = task_entry.get().strip()  # Убираем лишние пробелы
    if not task:
        messagebox.showwarning("Ошибка", "Нельзя добавить пустую задачу!")
        return
    existing_tasks = [task_tree.item(item, "text") for item in task_tree.get_children()]
    if task in existing_tasks:
        messagebox.showinfo("Информация", "Такая задача уже существует!")
        return
    task_tree.insert("", tk.END, text=task, values=(UNCHECKED,))
    task_entry.delete(0, tk.END)

def check_task(event):
    """Отметка задачи как выполненной или невыполненной."""
    item = task_tree.selection()[0]
    checked = task_tree.item(item, "values")[0]
    task_tree.item(item, values=(CHECKED if checked == UNCHECKED else UNCHECKED,))

def delete_task():
    """Удаление выбранной задачи."""
    selected_items = task_tree.selection()
    if not selected_items:
        messagebox.showwarning("Удаление задачи", "Выберите задачу для удаления!")
        return
    for item in selected_items:
        task_tree.delete(item)

def save_tasks():
    """Сохранение задач в файл."""
    tasks = [{"text": task_tree.item(item, "text"), "checked": task_tree.item(item, "values")[0]}
             for item in task_tree.get_children()]
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def load_tasks():
    """Загрузка задач из файла."""
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
        for task in tasks:
            task_tree.insert("", tk.END, text=task["text"], values=(task["checked"],))
    except FileNotFoundError:
        pass

# Интерфейс
root = tk.Tk()
root.title("Список задач")
root.geometry("400x550+800+300")
root.configure(bg="lightblue")

# Стили
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="lightblue", foreground="black", font=("Arial", 12))
style.configure("TButton", padding=10, font=("Arial", 10))
style.configure("Treeview", background="lightgray", foreground="black", rowheight=25, fieldbackground="lightgray")
style.map("Treeview", background=[("selected", "blue")])

# Виджеты
text1 = ttk.Label(root, text="Введите вашу задачу:")
text1.pack(pady=10)

task_entry = ttk.Entry(root, width=30)
task_entry.pack(pady=10)

add_task_button = ttk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.pack(pady=5)

text2 = ttk.Label(root, text="Список задач:")
text2.pack(pady=10)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_tree = ttk.Treeview(root, columns=("Готово",), displaycolumns=("Готово",))
task_tree.heading("#0", text="Задача")
task_tree.heading("Готово", text="Готово")
task_tree.column("#0", width=280)
task_tree.column("Готово", width=50, anchor="center")
task_tree.pack(pady=5, fill=tk.BOTH, expand=True)

task_tree.bind("<Double-1>", check_task)
task_tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_tree.yview)

delete_button = ttk.Button(root, text="Удалить задачу", command=delete_task)
delete_button.pack(pady=10)

# Загрузка и сохранение задач при закрытии
root.protocol("WM_DELETE_WINDOW", lambda: (save_tasks(), root.destroy()))
load_tasks()

# Запуск программы
root.mainloop()
