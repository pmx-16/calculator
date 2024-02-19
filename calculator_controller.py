"""Controller Module"""

class CalculatorController:
    """Controller for calculator"""
    def __init__(self, model, view):
        """Initialization"""
        self.model = model
        self.view = view
        self.view.set_key_press_callback(self.handle_key_press)

    def handle_key_press(self, key_value):
        """Method for handling pressed key"""
        if key_value in ['+', '-', '*', '/', '^', 'mod']:
            self.append_to_expression(key_value)
        elif key_value == '=':
            self.calculate_expression()
        elif key_value == 'DEL':
            self.delete_last_entry()
        elif key_value == 'C':
            self.clear_expression()
        elif key_value in ['exp', 'ln', 'log', 'log2', 'sqrt']:
            self.append_function(key_value)
        else:  # Handle numbers and decimal point
            self.append_to_expression(key_value)

    def append_to_expression(self, value):
        """Append a value to the expression."""
        current_display = self.view.display_value.get()
        updated_display = current_display + value
        self.view.display_value.set(updated_display)

    def calculate_expression(self):
        """Calculate the expression."""
        expression = self.view.display_value.get()
        result, successful = self.model.perform_calculation(expression)
        if successful:
            self.view.display_success()
            self.view.display_value.set(str(result))
            self.update_view_history()
        else:
            self.view.display_error("Invalid Expression")

    def delete_last_entry(self):
        """Delete the last entry in the expression."""
        current_display = self.view.display_value.get()

        # Check if the last entry is a function name
        function_names = ['exp', 'ln', 'log', 'log2', 'sqrt']
        for function in function_names:
            if current_display.endswith(function):
                self.view.display_value.set(current_display[:-len(function)])
                return

        # Check if the last entry is an operator
        operators = ['+', '-', '*', '/', '^']
        if current_display[-1] in operators:
            self.view.display_value.set(current_display[:-1])
            return
        self.view.display_value.set(current_display[:-1])

    def clear_expression(self):
        """Clear the expression."""
        self.view.display_value.set("")

    def append_function(self, function_name):
        """Append a function to the expression."""
        current_display = self.view.display_value.get()
        if current_display and current_display[-1] in "0123456789":
            updated_display = f"{function_name}({current_display})"
        else:
            updated_display = current_display + f"{function_name}("
        self.view.display_value.set(updated_display)

    def update_view_history(self):
        """Update the view's history."""
        self.view.update_history_view()
