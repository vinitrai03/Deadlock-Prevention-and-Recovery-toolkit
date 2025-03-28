# gui.py: GUI implementation using Tkinter
from tkinter import *
from tkinter import messagebox
from algorithms import DeadlockToolkit
from visualization import visualize_graph

class DeadlockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Prevention Toolkit")
        self.toolkit = None
        self.setup_interface()

    def setup_interface(self):
        """Initial setup screen."""
        self.setup_frame = LabelFrame(self.root, text="System Configuration", padx=10, pady=10)
        self.setup_frame.pack(padx=10, pady=10, fill="x")

        Label(self.setup_frame, text="Number of Processes:").grid(row=0, column=0, sticky="e")
        self.num_proc_entry = Entry(self.setup_frame)
        self.num_proc_entry.grid(row=0, column=1)
        Label(self.setup_frame, text="(e.g., 3)").grid(row=0, column=2)

        Label(self.setup_frame, text="Number of Resources:").grid(row=1, column=0, sticky="e")
        self.num_res_entry = Entry(self.setup_frame)
        self.num_res_entry.grid(row=1, column=1)
        Label(self.setup_frame, text="(e.g., 3)").grid(row=1, column=2)

        Button(self.setup_frame, text="Next", command=self.show_state_input).grid(row=2, column=0, columnspan=3, pady=5)

    def show_state_input(self):
        """Input initial state."""
        try:
            num_processes = int(self.num_proc_entry.get())
            num_resources = int(self.num_res_entry.get())
            if num_processes <= 0 or num_resources <= 0:
                raise ValueError("Must be positive integers.")
            self.toolkit = DeadlockToolkit(num_processes, num_resources)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive integers.")
            return

        self.setup_frame.destroy()
        self.state_frame = LabelFrame(self.root, text="Initial State Setup", padx=10, pady=10)
        self.state_frame.pack(padx=10, pady=10, fill="x")

        Label(self.state_frame, text="Allocation Matrix:").grid(row=0, column=0, columnspan=2)
        self.alloc_entries = []
        for p in range(self.toolkit.num_processes):
            Label(self.state_frame, text=f"P{p}:").grid(row=p+1, column=0, sticky="e")
            entry = Entry(self.state_frame)
            entry.grid(row=p+1, column=1)
            self.alloc_entries.append(entry)
            Label(self.state_frame, text=f"(e.g., {' '.join(['0'] * self.toolkit.num_resources)})").grid(row=p+1, column=2)

        row_start = self.toolkit.num_processes + 2
        Label(self.state_frame, text="Max Demand Matrix:").grid(row=row_start-1, column=0, columnspan=2)
        self.max_entries = []
        for p in range(self.toolkit.num_processes):
            Label(self.state_frame, text=f"P{p}:").grid(row=row_start+p, column=0, sticky="e")
            entry = Entry(self.state_frame)
            entry.grid(row=row_start+p, column=1)
            self.max_entries.append(entry)
            Label(self.state_frame, text=f"(e.g., {' '.join(['5'] * self.toolkit.num_resources)})").grid(row=row_start+p, column=2)

        Label(self.state_frame, text="Available Resources:").grid(row=row_start+self.toolkit.num_processes+1, column=0, sticky="e")
        self.available_entry = Entry(self.state_frame)
        self.available_entry.grid(row=row_start+self.toolkit.num_processes+1, column=1)
        Label(self.state_frame, text=f"(e.g., {' '.join(['2'] * self.toolkit.num_resources)})").grid(row=row_start+self.toolkit.num_processes+1, column=2)

        Button(self.state_frame, text="Start Toolkit", command=self.start_toolkit).grid(row=row_start+self.toolkit.num_processes+2, column=0, columnspan=3, pady=5)

    def start_toolkit(self):
        """Start the toolkit with initial state."""
        try:
            allocation = [[int(x) for x in entry.get().split()] for entry in self.alloc_entries]
            max_demand = [[int(x) for x in entry.get().split()] for entry in self.max_entries]
            available = [int(x) for x in self.available_entry.get().split()]

            if (len(allocation) != self.toolkit.num_processes or 
                any(len(row) != self.toolkit.num_resources for row in allocation) or
                len(max_demand) != self.toolkit.num_processes or 
                any(len(row) != self.toolkit.num_resources for row in max_demand) or
                len(available) != self.toolkit.num_resources):
                raise ValueError("Dimension mismatch in inputs.")
            
            self.toolkit.set_initial_state(allocation, max_demand, available)
            self.state_frame.destroy()
            self.show_main_interface()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def show_main_interface(self):
        """Main interface without resource request inputs."""
        self.main_frame = LabelFrame(self.root, text="Control Panel", padx=10, pady=10)
        self.main_frame.pack(padx=10, pady=5, fill="x")

        # Removed Process ID and Request fields
        Button(self.main_frame, text="Check Banker's Safety", command=self.check_bankers_safety).grid(row=0, column=0, pady=5)
        Button(self.main_frame, text="Detect Deadlock", command=self.detect_deadlock).grid(row=0, column=1, pady=5)
        Button(self.main_frame, text="Recover Deadlock", command=self.recover_deadlock).grid(row=1, column=0, pady=5)
        Button(self.main_frame, text="Visualize Graph", command=self.visualize).grid(row=1, column=1, pady=5)

        self.status_frame = LabelFrame(self.root, text="System Status", padx=10, pady=10)
        self.status_frame.pack(padx=10, pady=5, fill="x")

        self.status = Text(self.status_frame, height=4, width=50)
        self.status.pack()

        self.resource_info = Text(self.status_frame, height=3, width=50)
        self.resource_info.pack(pady=5)
        self.update_resource_info()

    def update_resource_info(self):
        """Update resource display."""
        self.resource_info.delete(1.0, END)
        self.resource_info.insert(END, f"Available: {self.toolkit.available}\n")
        self.resource_info.insert(END, f"Allocation:\n{self.toolkit.allocation}")

    def check_bankers_safety(self):
        """Display safety check result with safe sequence."""
        safe, message = self.toolkit.bankers_safety_check()
        self.status.delete(1.0, END)
        self.status.insert(END, message)
        self.status.config(fg="green" if safe else "red")
        self.update_resource_info()

    def detect_deadlock(self):
        """Check for deadlocks."""
        has_deadlock, cycles = self.toolkit.detect_deadlock()
        self.status.delete(1.0, END)
        self.status.insert(END, f"Deadlock Detected: {has_deadlock}\nDetails: {cycles}")
        self.status.config(fg="red" if has_deadlock else "green")
        self.update_resource_info()

    def recover_deadlock(self):
        """Recover from deadlock."""
        message = self.toolkit.recover_deadlock()
        self.status.delete(1.0, END)
        self.status.insert(END, message)
        self.status.config(fg="green")
        self.update_resource_info()

    def visualize(self):
        """Show resource allocation graph."""
        visualize_graph(self.toolkit)