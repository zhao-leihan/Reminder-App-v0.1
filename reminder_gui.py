import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

# Task Application Class
class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder Tugas dan Kegiatan")
        self.tasks = load_tasks()

        # Dark Mode with Gradient and Rounded Corners
        self.root.configure(bg='#2e2e2e')

        # UI Components
        self.frame = tk.Frame(root, bg='#2e2e2e', padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)

        # Title
        self.title_label = tk.Label(self.frame, text="Daftar Tugas", font=('Arial', 18, 'bold'), fg='white', bg='#2e2e2e')
        self.title_label.pack(pady=5)

        # Search Box with Modern Design
        self.search_label = tk.Label(self.frame, text="Cari Tugas", fg='white', bg='#2e2e2e', font=('Arial', 10))
        self.search_label.pack(pady=3)
        self.search_entry = tk.Entry(self.frame, bg='#3e3e3e', fg='white', font=('Arial', 10), bd=2, relief="solid", highlightthickness=1, highlightbackground="#4CAF50")
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_task)

        # Task Listbox with Rounded Corners and Hover Effect
        self.task_listbox = tk.Listbox(self.frame, width=50, height=8, bg='#3e3e3e', fg='white', selectbackground='#4CAF50', font=('Arial', 10), bd=2, relief="solid", highlightthickness=1, highlightbackground="#4CAF50")
        self.task_listbox.pack(pady=8)

        self.refresh_task_list()

        # Keterangan Tugas (Dikurangi Ukurannya)
        self.description_label = tk.Label(self.frame, text="Keterangan Tugas:", fg='white', bg='#2e2e2e', font=('Arial', 10))
        self.description_label.pack(pady=3)

        self.description_text = tk.Text(self.frame, width=30, height=2, bg='#3e3e3e', fg='white', font=('Arial', 10), wrap=tk.WORD)
        self.description_text.pack(pady=5)

        # Buttons with Hover Effect
        btn_frame = tk.Frame(self.frame, bg='#2e2e2e')
        btn_frame.pack(pady=8)

        self.add_button = tk.Button(btn_frame, text="Tambah Tugas", command=self.add_task, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.add_button.grid(row=0, column=0, padx=4)
        self.add_button.bind("<Enter>", self.on_hover_enter)
        self.add_button.bind("<Leave>", self.on_hover_leave)

        self.done_button = tk.Button(btn_frame, text="Tandai Selesai", command=self.mark_done, bg='#2196F3', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.done_button.grid(row=0, column=1, padx=4)
        self.done_button.bind("<Enter>", self.on_hover_enter)
        self.done_button.bind("<Leave>", self.on_hover_leave)

        self.delete_button = tk.Button(btn_frame, text="Hapus Tugas", command=self.delete_task, bg='#F44336', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.delete_button.grid(row=0, column=2, padx=4)
        self.delete_button.bind("<Enter>", self.on_hover_enter)
        self.delete_button.bind("<Leave>", self.on_hover_leave)

        self.edit_button = tk.Button(btn_frame, text="Edit Tugas", command=self.edit_task, bg='#FFC107', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.edit_button.grid(row=1, column=0, padx=4)
        self.edit_button.bind("<Enter>", self.on_hover_enter)
        self.edit_button.bind("<Leave>", self.on_hover_leave)

        self.sort_button = tk.Button(btn_frame, text="Sortir Deadline", command=self.sort_deadline, bg='#9C27B0', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.sort_button.grid(row=1, column=1, padx=4)
        self.sort_button.bind("<Enter>", self.on_hover_enter)
        self.sort_button.bind("<Leave>", self.on_hover_leave)

        self.filter_button = tk.Button(btn_frame, text="Filter Status", command=self.filter_status, bg='#00BCD4', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.filter_button.grid(row=1, column=2, padx=4)
        self.filter_button.bind("<Enter>", self.on_hover_enter)
        self.filter_button.bind("<Leave>", self.on_hover_leave)

        # Calendar widget for deadline input
        self.calendar_label = tk.Label(self.frame, text="Pilih Tanggal Deadline", fg='white', bg='#2e2e2e', font=('Arial', 12))
        self.calendar_label.pack(pady=6)

        self.calendar = Calendar(self.frame, selectmode='day', date_pattern='yyyy-mm-dd', font=('Arial', 10), background='lightblue', foreground='black', padding=4)
        self.calendar.pack(pady=6)

        # Grafik Button
        self.graph_button = tk.Button(self.frame, text="Tampilkan Grafik", command=self.show_graph, bg='#8E24AA', fg='white', font=('Arial', 12, 'bold'), relief="solid", width=16)
        self.graph_button.pack(pady=8)

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            status = "✅" if task['done'] else "❌"
            status_color = 'green' if task['done'] else 'red'
            self.task_listbox.insert(tk.END, f"{i+1}. [{status}] {task['title']} (Deadline: {task['deadline']})")
            self.task_listbox.itemconfig(i, {'bg': status_color})

    def add_task(self):
        title = simpledialog.askstring("Tambah Tugas", "Nama tugas:")
        deadline = self.calendar.get_date()
        description = simpledialog.askstring("Deskripsi Tugas", "Deskripsi tugas:")
        if title and deadline and description:
            self.tasks.append({"title": title, "deadline": deadline, "done": False, "description": description})
            save_tasks(self.tasks)
            self.refresh_task_list()

    def mark_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]['done'] = True
            save_tasks(self.tasks)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Peringatan", "Pilih tugas yang ingin ditandai selesai.")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            save_tasks(self.tasks)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Peringatan", "Pilih tugas yang ingin dihapus.")

    def edit_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            new_title = simpledialog.askstring("Edit Tugas", f"Edit nama tugas ({self.tasks[index]['title']}):")
            new_deadline = self.calendar.get_date()
            new_description = simpledialog.askstring("Edit Deskripsi", f"Edit deskripsi tugas ({self.tasks[index]['description']}):")
            if new_title and new_deadline and new_description:
                self.tasks[index]['title'] = new_title
                self.tasks[index]['deadline'] = new_deadline
                self.tasks[index]['description'] = new_description
                save_tasks(self.tasks)
                self.refresh_task_list()
        else:
            messagebox.showwarning("Peringatan", "Pilih tugas yang ingin diedit.")

    def sort_deadline(self):
        self.tasks.sort(key=lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d'))
        save_tasks(self.tasks)
        self.refresh_task_list()

    def filter_status(self):
        status = simpledialog.askstring("Filter Status", "Masukkan status (selesai/belum selesai):")
        if status:
            filtered_tasks = [task for task in self.tasks if ("selesai" in status and task['done']) or ("belum selesai" in status and not task['done'])]
            self.tasks = filtered_tasks
            self.refresh_task_list()

    def search_task(self, event):
        search_term = self.search_entry.get().lower()
        filtered_tasks = [task for task in self.tasks if search_term in task['title'].lower()]
        self.tasks = filtered_tasks
        self.refresh_task_list()

    def show_graph(self):
        completed = sum(1 for task in self.tasks if task['done'])
        not_completed = len(self.tasks) - completed

        # Pie chart for task completion
        labels = 'Selesai', 'Belum Selesai'
        sizes = [completed, not_completed]
        colors = ['#4CAF50', '#F44336']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Statistik Penyelesaian Tugas')
        plt.show()

    def on_hover_enter(self, event):
        event.widget.config(bg="#45a049")

    def on_hover_leave(self, event):
        event.widget.config(bg="#4CAF50")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
 