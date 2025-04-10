import tkinter as tk
from tkinter import messagebox
import json
import os
import speech_recognition as sr
from plyer import notification

TASK_FILE = "daily_tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Get voice input from microphone
def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Speak your task...")
        audio = recognizer.listen(source)
    try:
        task = recognizer.recognize_google(audio)
        return task
    except:
        messagebox.showerror("Error", "Couldn't understand you!")
        return None

# Show a system notification
def show_notification(task):
    notification.notify(
        title="📌 Task Reminder",
        message=task,
        timeout=5
    )

# Main app class
class PlannerApp:
    def __init__(self, master):
        self.master = master
        master.title("📝 Smart Daily Planner")
        master.geometry("400x500")

        self.tasks = load_tasks()

        self.label = tk.Label(master, text="Today's Tasks", font=("Arial", 16))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(master, width=40, height=15, font=("Arial", 12))
        self.listbox.pack(pady=5)

        self.entry = tk.Entry(master, font=("Arial", 12), width=25)
        self.entry.pack(pady=5)

        self.add_btn = tk.Button(master, text="Add Task", command=self.add_task, font=("Arial", 11))
        self.add_btn.pack(pady=5)

        self.voice_btn = tk.Button(master, text="🎤 Add Task by Voice", command=self.add_task_voice, font=("Arial", 11))
        self.voice_btn.pack(pady=5)

        self.done_btn = tk.Button(master, text="Mark Done", command=self.mark_done, font=("Arial", 11))
        self.done_btn.pack(pady=5)

        self.notify_btn = tk.Button(master, text="🔔 Notify About Task", command=self.remind_task, font=("Arial", 11))
        self.notify_btn.pack(pady=5)

        self.load_listbox()

    def load_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✅" if task["done"] else "🔲"
            self.listbox.insert(tk.END, f"{status} {task['task']}")

    def add_task(self):
        task_text = self.entry.get()
        if task_text:
            self.tasks.append({"task": task_text, "done": False})
            self.entry.delete(0, tk.END)
            self.load_listbox()
            save_tasks(self.tasks)

    def add_task_voice(self):
        task_text = get_speech_input()
        if task_text:
            self.tasks.append({"task": task_text, "done": False})
            self.load_listbox()
            save_tasks(self.tasks)

    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            self.tasks[index]["done"] = True
            self.load_listbox()
            save_tasks(self.tasks)
        except IndexError:
            messagebox.showwarning("Oops!", "Select a task to mark as done.")

    def remind_task(self):
        try:
            index = self.listbox.curselection()[0]
            task = self.tasks[index]["task"]
            show_notification(task)
        except IndexError:
            messagebox.showwarning("Oops!", "Select a task to notify.")

# Run the app
root = tk.Tk()
app = PlannerApp(root)
root.mainloop()
