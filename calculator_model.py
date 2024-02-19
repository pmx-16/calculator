class CalculatorModel:
    def __init__(self):
        self.history = []

    def perform_calculation(self, expression):
        try:
            # Replace python math functions with equivalent expressions
            expression = expression.replace('^', '**')
            expression = expression.replace('sqrt', 'math.sqrt')
            expression = expression.replace('ln', 'math.log')
            expression = expression.replace('log', 'math.log10')
            expression = expression.replace('log2', 'math.log2')

            # Evaluate the expression
            result = eval(expression, {"__builtins__": None}, {"math": __import__('math')})

            self.history.append(f"{expression} = {result}")
            return result, True

        except Exception as e:
            # Return the error message, but do not add to history
            return f"Error: {str(e)}", False

    def get_history(self):
        return self.history
