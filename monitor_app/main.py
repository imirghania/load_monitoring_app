import time
import tkinter as tk
from tkinter import ttk

import psutil
import pytz
from tzlocal import get_localzone

from monitor_app.database import SystemRecord, session
from monitor_app.settings import settings


# GUI Application
class SystemMonitorApp:
    def __init__(self, root, session):
        self.session = session
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("300x200")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)  
        self.root.grid_columnconfigure(1, weight=1)  

        self.is_recording = False
        self.update_interval = int(settings.update_interval)
        self.start_time = None

        self.create_ui()
        self.update_stats()


    def create_ui(self):
        content = ttk.Frame(self.root, padding=3)
        content.grid(column=0, row=0, sticky='nsew')
        
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)  
        content.grid_columnconfigure(0, weight=1)  
        content.grid_columnconfigure(1, weight=1)  
        
        # Metrics
        self.cpu_label = ttk.Label(content, text="CPU: 0%")
        self.cpu_label.grid(row=0, column=0, columnspan=2, padx=10, pady=1, sticky="w")

        self.ram_label = ttk.Label(content, text="RAM: Free/Total")
        self.ram_label.grid(row=1, column=0, columnspan=2, padx=10, pady=1, sticky="w")

        self.storage_label = ttk.Label(content, text="STORAGE: Free/Total")
        self.storage_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(1, 5), sticky="w")

        # History button
        self.history_button = tk.Button(
            content,
            text="📃",
            font=("Arial", 12),
            bg="gray",
            fg="white",
            command=self.view_history,
            relief="flat",
            width=3,
            height=1,
            )
        self.history_button.grid(row=0, column=4, padx=10, pady=5, sticky="ne")

        # Timer label
        self.timer_label = ttk.Label(content, text="00:00")

        # Start/Stop button
        self.start_button = tk.Button(
            content,
            text="START RECORDING",
            font=("Arial", 12, "bold"),
            command=self.start_recording,
            bg="gray",
            fg="white",
            width=17,
            relief="flat",
            padx=5,
            pady=2
            )
        self.start_button.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="wes")

        self.stop_button = tk.Button(
            content,
            text="STOP RECORDING",
            font=("Arial", 12, "bold"),
            command=self.stop_recording,
            bg="gray",
            fg="white",
            width=17,
            relief="flat",
            padx=5,
            pady=2
        )
        self.stop_button.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="wes")
        self.stop_button.grid_remove()  # Hide initially


    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        storage = psutil.disk_usage('/')

        self.cpu_label.config(text=f"CPU: {cpu}%")
        self.ram_label.config(text=f"RAM: {round(ram.available / (1024**3), 1)}GB/{ram.total // (1024**3)}GB")
        self.storage_label.config(text=f"Storage: {round(storage.free / (1024**3), 1)}GB/{storage.total // (1024**3)}GB")

        if self.is_recording:
            self.record_data(cpu, ram.percent, storage.percent)
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"{elapsed_time // 60:02}:{elapsed_time % 60:02}")

        self.root.after(self.update_interval, self.update_stats)


    def start_recording(self):
        self.is_recording = True
        self.start_time = time.time()
        self.start_button.grid_remove()
        self.stop_button.grid()
        self.timer_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="s")


    def stop_recording(self):
        self.is_recording = False
        self.start_button.grid()
        self.stop_button.grid_remove()
        self.timer_label.config(text="00:00")
        self.timer_label.grid_remove()


    def record_data(self, cpu, ram, storage):
        record = SystemRecord(cpu_load=cpu, ram_load=ram, storage_load=storage)
        self.session.add(record)
        self.session.commit()


    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Recorded data")
        tree = ttk.Treeview(history_window, columns=('Time', 'CPU', 'RAM', 'STORAGE'), show='headings')
        tree.heading('Time', text='Time')
        tree.heading('CPU', text='CPU %')
        tree.heading('RAM', text='RAM %')
        tree.heading('STORAGE', text='STORAGE %')
        tree.grid(row=0, column=0, padx=10, pady=5)
        
        local_timezone = pytz.timezone(get_localzone().key)

        records = self.session.query(SystemRecord).all()
        for record in records:
            tree.insert('', 'end', 
                        values=(
                            record.time.replace(
                                tzinfo=pytz.utc
                                ).astimezone(tz=local_timezone), 
                            record.cpu_load, 
                            record.ram_load, 
                            record.storage_load
                            )
                        )


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root, session)
    root.mainloop()

