import tkinter as tk

# Keypad should extend Frame so that it is a container
class Keypad(tk.Frame):
    """
    A customizable keypad component for application
    """
    def __init__(self, parent, keynames=[], columns=1, **kwargs):
        # call the superclass constructor with all args except
		# keynames and columns
        super().__init__(parent, **kwargs)
        self.keynames = keynames
        self.buttons = []
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        for i, keyname in enumerate(self.keynames):
            if keyname.strip():
                button = tk.Button(self, text=keyname)
                button.grid(row=i // columns, column=i % columns, sticky=tk.NSEW)
                self.buttons.append(button)
                self.rowconfigure(i // columns, weight=1)
            self.columnconfigure(i % columns, weight=1)

    def bind(self, sequence, func, add=None):
        """Bind an event handler to an event sequence."""
        # Write a bind method with exactly the same parameters
        # as the bind method of Tkinter widgets.
        # Use the parameters to bind all the buttons in the keypad
        # to the same event handler.
        for button in self.buttons:
            button.bind(sequence, func, add)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for button in self.buttons:
            button[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        return [button[key] for button in self.buttons]

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        for button in self.buttons:
            button.configure(cnf, **kwargs)

    # Write a property named 'frame' the returns a reference to
    # the superclass object for this keypad.
    # This is so that a programmer can set properties of a keypad's frame,
    # e.g. keypad.frame.configure(background='blue')

    @property
    def frame(self):
        """return a reference to the superclass object"""
        return self

if __name__ == '__main__':
    keys = list('789456123 0.')  # = ['7','8','9',...]

    root = tk.Tk()
    root.title("Keypad Demo")
    keypad = Keypad(root, keynames=keys, columns=3)
    keypad.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
