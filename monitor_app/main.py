import tkinter as tk
from tkinter import ttk


# GUI Application
class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("300x200")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)  
        self.root.grid_columnconfigure(1, weight=1)
        
        self.create_ui()


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
        self.stop_button.grid_remove()
    
    
    def start_recording(self):
        ...


    def stop_recording(self):
        ...
        
    
    def view_history(self):
        ...


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
