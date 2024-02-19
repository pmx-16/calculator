class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_key_press_callback(self.handle_key_press)

    def handle_key_press(self, key_value):
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
        current_display = self.view.display_value.get()
        updated_display = current_display + value
        self.view.display_value.set(updated_display)

    def calculate_expression(self):
        expression = self.view.display_value.get()
        result, successful = self.model.perform_calculation(expression)
        if successful:
            self.view.display_value.set(str(result))
            self.update_view_history()
        else:
            self.view.display_error("Invalid Expression")

    def delete_last_entry(self):
        current_display = self.view.display_value.get()
        self.view.display_value.set(current_display[:-1])

    def clear_expression(self):
        self.view.display_value.set("")

    def append_function(self, function_name):
        current_display = self.view.display_value.get()
        if current_display and current_display[-1] in "0123456789":
            updated_display = f"{function_name}({current_display})"
        else:
            updated_display = current_display + f"{function_name}("
        self.view.display_value.set(updated_display)

    def update_view_history(self):
        self.view.update_history_view()
