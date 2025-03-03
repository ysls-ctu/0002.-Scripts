import tkinter as tk
from datetime import datetime, timedelta

class BreakToolApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("180x450")
        self.root.title("Breaks 1.5.4")
        self.root.attributes('-toolwindow', True)
        self.root.resizable(False, False)
        
        self.b1_in_timestamp = None
        self.b1_out_timestamp = None
        self.lunch_in_timestamp = None
        self.lunch_out_timestamp = None
        self.b2_in_timestamp = None
        self.b2_out_timestamp = None
        self.buttons = []
        
        self.create_menu()
        self.create_labels()
        self.create_buttons()
        self.configure_grid()
        
        self.titletag_label = tk.Label(self.root, text="BREAK", font=("Arial", 20, "bold"), fg="red")
        self.titletag_label.grid(row=15, column=0, columnspan=2, pady=1, sticky='ew')
        self.titletag_label.grid_remove()
        
        self.color_change_id = None
        self.change_title_color()

    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.grid(row=0, column=0, columnspan=3)
        
        user_label = tk.Button(menu_frame, text="User", relief="flat")
        tools_label = tk.Label(menu_frame, text="Tools", padx=5)
        reports_label = tk.Label(menu_frame, text="Reports", padx=5)
        arrow_label = tk.Label(menu_frame, text=">>", padx=5)
        
        user_label.grid(row=0, column=0)
        tools_label.grid(row=0, column=1)
        reports_label.grid(row=0, column=2)
        arrow_label.grid(row=0, column=3)

    def create_labels(self):
        name = "Yancy Salas"
        name_label = tk.Label(self.root, text=name, font=("Calibri", 10, "bold"))
        name_label.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        ot_code_entry = tk.Entry(self.root, width=10, bd=1, relief="solid")
        ot_code_entry.grid(row=8, column=1, padx=5)
        ot_code_label = tk.Label(self.root, text="OT CODE", font=("Arial", 8))
        ot_code_label.grid(row=9, column=1, padx=5)

    def create_buttons(self):
        self.b1_in_button = self.create_button("Break 1 - In", 2, 0, self.b1_in_onclick, state=tk.NORMAL)
        self.b1_out_button = self.create_button("Break 1 - Out", 3, 0, self.b1_out_onclick, state=tk.NORMAL)
        self.lunch_in_button = self.create_button("Lunch - In", 4, 0, self.lunch_in_onclick, state=tk.NORMAL)
        self.lunch_out_button = self.create_button("Lunch - Out", 5, 0, self.lunch_out_onclick, state=tk.NORMAL)
        self.b2_in_button = self.create_button("Break 2 - In", 6, 0, self.b2_in_onclick, state=tk.DISABLED)
        self.b2_out_button = self.create_button("Break 2 - Out", 7, 0, self.b2_out_onclick, state=tk.DISABLED)
        self.ot_in_button = self.create_button("OT - In", 8, 0, lambda: None, state=tk.NORMAL)
        self.ot_out_button = self.create_button("OT - Out", 9, 0, lambda: None, state=tk.NORMAL)
        self.personal_time_in_button = self.create_button("Personal\nTime In", 12, 0, lambda: None, width=9, height=2, state=tk.NORMAL)
        self.personal_time_out_button = self.create_button("Personal\nTime Out", 12, 1, lambda: None, width=9, height=2, state=tk.NORMAL)
        self.company_time_in_button = self.create_button("Company\nTime In", 13, 0, lambda: None, width=9, height=2, state=tk.NORMAL)
        self.company_time_out_button = self.create_button("Company\nTime Out", 13, 1, lambda: None, width=9, height=2, state=tk.NORMAL)

        self.buttons = [
            self.b1_in_button,
            self.b1_out_button,
            self.lunch_in_button,
            self.lunch_out_button,
            self.b2_in_button,
            self.b2_out_button,
            self.ot_in_button,
            self.ot_out_button,
            self.personal_time_in_button,
            self.personal_time_out_button,
            self.company_time_in_button,
            self.company_time_out_button
        ]
    
    def create_button(self, text, row, col, command, width=12, height=1, padx=5, pady=1, state=tk.NORMAL):
        button = tk.Button(
            self.root,
            text=text,
            width=width,
            height=height,
            font=("Calibri", 10),
            state=state,
            relief="groove",
            bd=2,
            bg="SystemButtonFace",
            fg="black",
            command=command
        )

        button.grid(row=row, column=col, padx=padx, pady=pady)
        return button


    def configure_grid(self):
        for i in range(3):  # For columns 0 to 2
            self.root.grid_columnconfigure(i, weight=1)
        
        for i in range(16):  # For rows 0 to 15
            self.root.grid_rowconfigure(i, weight=1)

    def on_click(self):
        print("Button clicked")
    
    def b1_in_onclick(self):
        self.b1_in_timestamp = (datetime.now() + timedelta(hours=12)).strftime('%H:%M:%S')
        b1_in_label = tk.Label(self.root, text=self.b1_in_timestamp, font=("Arial", 8))
        b1_in_label.grid(row=2, column=1, padx=0)
        self.titletag_label.grid()
        self.titletag_label.grid(row=15, column=0, columnspan=2, pady=1, sticky='ew')
        
        buttons_to_enable = [
            self.b1_in_button,
            self.b1_out_button
        ]

        for button in self.buttons:
            if button in buttons_to_enable:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)

    def b1_out_onclick(self):
        self.b1_out_timestamp = (datetime.now() + timedelta(hours=12)).strftime('%H:%M:%S')
        b1_out_label = tk.Label(self.root, text=self.b1_out_timestamp, font=("Arial", 8))
        b1_out_label.grid(row=3, column=1, padx=0)
        self.titletag_label.grid_forget()

        for button in self.buttons:
            button.config(state=tk.NORMAL)
    
    def lunch_in_onclick(self):
        self.lunch_in_timestamp = (datetime.now() + timedelta(hours=12)).strftime('%H:%M:%S')
        lunch_in_label = tk.Label(self.root, text=self.lunch_in_timestamp, font=("Arial", 8))
        lunch_in_label.grid(row=4, column=1, padx=0)
        self.titletag_label.grid()
        self.titletag_label.config(text="LUNCH")
        self.titletag_label.grid(row=15, column=0, columnspan=2, pady=1, sticky='ew')
        
        buttons_to_enable = [
            self.lunch_in_button,
            self.lunch_out_button,
        ]

        for button in self.buttons:
            if button in buttons_to_enable:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)

    def lunch_out_onclick(self):
        self.lunch_out_timestamp = (datetime.now() + timedelta(hours=12)).strftime('%H:%M:%S')
        lunch_out_label = tk.Label(self.root, text=self.lunch_out_timestamp, font=("Arial", 8))
        lunch_out_label.grid(row=5, column=1, padx=0)
        self.titletag_label.grid_forget()

        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def b2_in_onclick(self):
        self.b2_in_timestamp = (datetime.now() + timedelta(hours=12)).strftime('%H:%M:%S')
        b2_in_label = tk.Label(self.root, text=self.b2_in_timestamp, font=("Arial", 8))
        b2_in_label.grid(row=6, column=1, padx=0)
        self.titletag_label.grid()
        self.titletag_label.config(text="BREAK")
        self.titletag_label.grid(row=15, column=0, columnspan=2, pady=1, sticky='ew')
        
        buttons_to_enable = [
            self.b2_in_button,
            self.b2_out_button,
        ]

        for button in self.buttons:
            if button in buttons_to_enable:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)

    def b2_out_onclick(self):
        self.b2_out_timestamp = (datetime.now() + timedelta(hours=12)).strftime('%H:%M:%S')
        b2_out_label = tk.Label(self.root, text=self.b2_out_timestamp, font=("Arial", 8))
        b2_out_label.grid(row=7, column=1, padx=0)
        self.titletag_label.grid_forget()

        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def change_title_color(self):
        current_color = self.titletag_label.cget("fg")
        new_color = "light grey" if current_color == "red" else "red"
        self.titletag_label.config(fg=new_color)
        self.color_change_id = self.root.after(2000, self.change_title_color)

    def stop_color_change(self):
        if self.color_change_id is not None:
            self.root.after_cancel(self.color_change_id)
            self.color_change_id = None
            self.titletag_label.config(fg="SystemButtonFace")

if __name__ == "__main__":
    root = tk.Tk()
    app = BreakToolApp(root)
    root.mainloop()