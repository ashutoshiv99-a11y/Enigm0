import tkinter as tk
from tkinter import ttk

class UIRedesign:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S. UI Redesign")
        self.root.geometry("800x600")
        self.root.configure(background="#2b2b2b")

        # Create main frame
        self.main_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.main_frame.pack(fill="both", expand=True)

        # Create header frame
        self.header_frame = tk.Frame(self.main_frame, bg="#4b4b4b")
        self.header_frame.pack(fill="x")

        # Create header label
        self.header_label = tk.Label(self.header_frame, text="J.A.R.V.I.S.", font=("Arial", 24), bg="#4b4b4b", fg="#ffffff")
        self.header_label.pack(pady=10)

        # Create content frame
        self.content_frame = tk.Frame(self.main_frame, bg="#2b2b2b")
        self.content_frame.pack(fill="both", expand=True)

        # Create tab control
        self.tab_control = ttk.Notebook(self.content_frame)
        self.tab_control.pack(fill="both", expand=True)

        # Create tabs
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text="Home")
        self.tab_control.add(self.tab2, text="Skills")
        self.tab_control.add(self.tab3, text="Settings")

        # Create home tab content
        self.home_label = tk.Label(self.tab1, text="Welcome to J.A.R.V.I.S.", font=("Arial", 18), bg="#2b2b2b", fg="#ffffff")
        self.home_label.pack(pady=20)

        # Create skills tab content
        self.skills_label = tk.Label(self.tab2, text="Skills:", font=("Arial", 18), bg="#2b2b2b", fg="#ffffff")
        self.skills_label.pack(pady=20)

        # Create settings tab content
        self.settings_label = tk.Label(self.tab3, text="Settings:", font=("Arial", 18), bg="#2b2b2b", fg="#ffffff")
        self.settings_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    ui_redesign = UIRedesign(root)
    root.mainloop()