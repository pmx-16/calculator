"""View Module"""

import tkinter as tk
from tkinter import ttk
from keypad import Keypad

class CalculatorUI(tk.Tk):
    """Ui for Calculator(View)"""
    def __init__(self):
        """Initialization"""
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
        """Handle a key press event."""
        if self.key_press_callback:
            self.key_press_callback(event.widget.cget("text"))

    def init_components(self):
        """Initialize all UI components."""
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
        self.math_operations.bind("<<ComboboxSelected>>", self.update_display_from_combobox)

        # Create keypad
        numeric_keys = list('789456123C0.')  # Number keys
        self.numeric_keypad = Keypad(self, keynames=numeric_keys, columns=3)
        self.numeric_keypad.grid(row=3, column=0, sticky=tk.NSEW, padx=0, pady=0)

        # Create operator pad
        operator_keys = list('/*-+^')  # Operator keys
        self.operator_keypad = Keypad(self, keynames=operator_keys, columns=1)
        self.operator_keypad.grid(row=3, column=3, sticky=tk.NSEW, padx=0, pady=0)

        # Create operator pad2
        operator_keys2 = ['DEL','(',')','MOD','=']  # Operator keys2
        self.operator_keypad2 = Keypad(self, keynames=operator_keys2, columns=1)
        self.operator_keypad2.grid(row=3, column=4, sticky=tk.NSEW, padx=0, pady=0)

        # Bind events and configure styles for all keys
        self.numeric_keypad.bind("<Button-1>", self.key_pressed)
        self.operator_keypad.bind("<Button-1>", self.key_pressed)
        self.operator_keypad2.bind("<Button-1>", self.key_pressed)

        # Set the minimum size for the window
        self.minsize(200, 300)  # Width, Height

        # Configure the row and column weights to make the keypad expandable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(3, weight=1)

    def set_key_press_callback(self, callback):
        """Set the key press callback."""
        self.key_press_callback = callback

    def display_error(self, message):
        """Display an error message, and set text color to red"""
        self.display_value.set(message)
        self.display.config(fg='red')

    def display_success(self):
        """Reset the text color to black after successful computation."""
        self.display.config(fg='black')

    def update_history_view(self):
        """Update the history listbox with calculation history."""
        self.history_listbox.delete(0, tk.END)
        for entry in self.model.get_history():
            self.history_listbox.insert(tk.END, entry)

    def update_display_from_combobox(self, event):
        """Update the display based on the selected operation from the combobox."""
        selected_operation = self.math_operations.get()
        current_display = self.display_value.get()

        if selected_operation:
            if current_display.endswith(('+', '-', '*', '/', '^', '(')):
                self.display_value.set(current_display + selected_operation + '(')
            elif current_display and current_display[-1].isdigit():
                self.display_value.set(current_display + '*' + selected_operation + '(')
            else:
                self.display_value.set(current_display + selected_operation + '(')

    def run(self):
        """Run the calculator"""
        self.mainloop()
