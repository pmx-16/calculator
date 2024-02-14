import tkinter as tk
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
  
        # Create keypad
        numeric_keys = list('789456123 0.')  # Number keys
        self.numeric_keypad = Keypad(self, keynames=numeric_keys, columns=3)
        self.numeric_keypad.grid(row=1, column=0, sticky=tk.NSEW, padx=0, pady=0)

        # Create operator pad
        operator_keys = list('/*-+^=')  # Operator keys
        self.operator_keypad = Keypad(self, keynames=operator_keys, columns=1)
        self.operator_keypad.grid(row=1, column=3, sticky=tk.NSEW, padx=0, pady=0)

        # Bind events and configure styles for all keys
        self.numeric_keypad.bind("<Button-1>", self.key_pressed)
        self.operator_keypad.bind("<Button-1>", self.key_pressed)

        # Set the minimum size for the window
        self.minsize(300, 400)  # Width, Height

        # Configure the row and column weights to make the keypad expandable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(3, weight=1)

    def run(self):
        self.mainloop()
