import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading
from plyer import notification



# Создаем основной класс для приложения
class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Автопланировщик")
        self.root.geometry("900x900")
        # self.root.iconbitmap(r"C:\Users\user\Desktop\cryptocurrencies_binance_coin_money_icon_210259.ico")

        # Список задач
        self.tasks = []

        # Поле для добавления задачи и времени
        self.task_label = tk.Label(root, text="Задача:")
        self.task_label.pack()

        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.pack()

        self.time_label = tk.Label(root, text="Время (HH:MM):")
        self.time_label.pack()

        self.time_entry = tk.Entry(root, width=30)
        self.time_entry.pack()

        # Кнопки
        self.add_button = tk.Button(root, text="Добавить задачу", command=self.add_task)
        self.add_button.pack()

        self.view_button = tk.Button(root, text="Просмотреть задачи", command=self.view_tasks)
        self.view_button.pack()

        # Запускаем автопланировщик в отдельном потоке
        self.auto_scheduler_thread = threading.Thread(target=self.auto_scheduler)
        self.auto_scheduler_thread.start()

    # Функция для добавления задач
    def add_task(self):
        task = self.task_entry.get()
        time_str = self.time_entry.get()

        # Проверка на корректность времени
        try:
            task_time = datetime.strptime(time_str, "%H:%M").time()
            self.tasks.append({"task": task, "time": task_time})
            self.tasks = sorted(self.tasks, key=lambda x: x["time"])  # Сортировка задач по времени
            messagebox.showinfo("Успех", f"Задача '{task}' добавлена на {time_str}")
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите время в формате HH:MM")

    # Функция для просмотра задач
    def view_tasks(self):
        tasks_window = tk.Toplevel(self.root)

        tasks_window.title("Список задач")
        tasks_window.geometry("600x600")

        for task in self.tasks:
            task_label = tk.Label(tasks_window, text=f"{task['time'].strftime('%H:%M')} - {task['task']}")
            task_label.pack()

    # Автопланировщик для уведомлений
    def auto_scheduler(self):
        while True:
            now = datetime.now().time()
            for task in self.tasks:
                task_time = task["time"]
                if task_time.hour == now.hour and task_time.minute == now.minute:
                    self.show_notification(task["task"])
                    time.sleep(60)  # Пауза на минуту, чтобы не было повторных уведомлений
            time.sleep(20)  # Проверка каждые 20 секунд

    # Функция для показа уведомлений
    def show_notification(self, task):
        notification.notify(
            title="Напоминание о задаче",
            message=f"Время для задачи: {task}",
            timeout=10
        )


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()

