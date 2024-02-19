import tkinter as tk
from tkinter import ttk
from keypad import Keypad

class CalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.display_value = tk.StringVar()
        self.init_components()

    def make_keypad(self) -> tk.Frame:
        """Create a frame containing buttons for the numbers keys."""
        frame = tk.Frame(self)
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 1), ('.', 3, 2)
        ]
        for (text, row, column) in buttons:
            button = tk.Button(frame, text=text, command=lambda val=text: self.key_pressed(val))
            options = {'sticky': tk.NSEW, 'padx': 2, 'pady': 2}
            button.grid(row=row, column=column, **options)

        # Configure weights for rows and columns
        for i in range(4):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i, weight=1)

        return frame

    def make_operator_pad(self) -> tk.Frame:
        """Create a frame containing buttons for the operator keys."""
        frame = tk.Frame(self)
        operators = [
            ('/', 0, 0), ('*', 1, 0),
            ('-', 2, 0), ('+', 3, 0),
            ('^', 4, 0), ('=', 5, 0)
        ]
        for (text, row, column) in operators:
            button = tk.Button(frame, text=text, command=lambda val=text: self.key_pressed(val))
            options = {'sticky': tk.NSEW}
            button.grid(row=row, column=column, **options)

        # Configure weights for rows and columns
        for i in range(3):
            frame.rowconfigure(i, weight=1)
        frame.columnconfigure(0, weight=1)

        return frame

    def key_pressed(self, event):
        # Get the button's text
        pressed_key = event.widget['text']
         # Concatenate the pressed key to the current value in the display
        current_value = self.display_value.get()
        new_value = current_value + pressed_key
        self.display_value.set(new_value)


    def init_components(self):
        # Create and configure the display
        self.display = tk.Entry(self, textvariable=self.display_value,
                                justify='right', state='readonly', font=('Arial', 24))
        self.display.grid(row=0, column=0, columnspan=4, sticky=tk.EW, padx=10, pady=10)

        # Add history listbox
        self.history_listbox = tk.Listbox(self, height=1)
        self.history_listbox.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # Add combobox for extra mathematical operations
        self.math_operations = ttk.Combobox(self, values=["exp", "ln", "log", "log2", "sqrt"])
        self.math_operations.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        self.math_operations.bind("<<ComboboxSelected>>")

        # Create keypad
        numeric_keys = list('789456123C0.')  # Number keys
        self.numeric_keypad = Keypad(self, keynames=numeric_keys, columns=3)
        self.numeric_keypad.grid(row=3, column=0, sticky=tk.NSEW, padx=0, pady=0)

        # Create operator pad
        operator_keys = list('/*-+^=')  # Operator keys
        self.operator_keypad = Keypad(self, keynames=operator_keys, columns=1)
        self.operator_keypad.grid(row=3, column=3, sticky=tk.NSEW, padx=0, pady=0)

        # Bind events and configure styles for all keys
        self.numeric_keypad.bind("<Button-1>", self.key_pressed)
        self.operator_keypad.bind("<Button-1>", self.key_pressed)

        # Set the minimum size for the window
        self.minsize(300, 400)  # Width, Height

        # Configure the row and column weights to make the keypad expandable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(3, weight=1)

    def load_history(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_text = event.widget.get(index)
            expression = selected_text.split(' = ')[0]
            self.display_value.set(expression)

    def set_key_press_callback(self, callback):
        self.key_press_callback = callback

    def on_button_press(self, value):
        if self.key_press_callback:
            self.key_press_callback(value)

    def display_error(self, message):
        self.display_value.set(message)
        self.display.config(fg='red')

    def update_history_view(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.model.get_history():
            self.history_listbox.insert(tk.END, entry)

    def run(self):
        self.mainloop()
