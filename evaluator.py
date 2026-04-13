import math

def evaluate(postfix_expression, symbol_table):
    stack = []
    operators = {'+', '-', '*', '/', '^', 'mod', 'div', 'neg'}
    functions = {'sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'abs', 'sqr', 'arctan'}

    for token in postfix_expression:
        try:
            if isinstance(token, (int, float)):
                stack.append(float(token))
            elif isinstance(token, str) and token.isnumeric():
                stack.append(float(token))
            elif token in operators:
                if token == 'neg':
                    if not stack:
                        raise ValueError(f"Missing operand for operator '{token}'")
                    operand = stack.pop()
                    stack.append(-operand)
                else:
                    if len(stack) < 2:
                        raise ValueError(f"Missing operands for operator '{token}'")
                    right = stack.pop()
                    left = stack.pop()
                    if token == '+':
                        stack.append(left + right)
                    elif token == '-':
                        stack.append(left - right)
                    elif token == '*':
                        stack.append(left * right)
                    elif token == '/':
                        if right == 0:
                            raise ZeroDivisionError("Division by zero is undefined.")
                        stack.append(left / right)
                    elif token == '^':
                        stack.append(left ** right)
                    elif token == 'mod':
                        if not right.is_integer() or not left.is_integer(): 
                            raise ValueError("Modulo operation requires integer operands.")
                        if right == 0:
                            raise ZeroDivisionError("Modulo by zero is undefined.")
                        stack.append(left % right)
                    elif token == 'div':
                        if not right.is_integer() or not left.is_integer(): 
                            raise ValueError("Modulo operation requires integer operands.")
                        if right == 0:
                            raise ZeroDivisionError("Division by zero is undefined.")
                        stack.append(left // right)
                    else:
                        raise ValueError(f"Unknown operator '{token}'.")
            elif token in functions:
                if not stack:
                    raise ValueError(f"Missing operand for function '{token}'")
                operand = stack.pop()
                try:
                    if token == 'sin':
                        stack.append(math.sin(math.radians(operand)))
                    elif token == 'cos':
                        stack.append(math.cos(math.radians(operand)))
                    elif token == 'tan':
                        stack.append(math.tan(math.radians(operand)))
                    elif token == 'log':
                        if operand <= 0:
                            raise ValueError("Logarithm undefined for non-positive values.")
                        stack.append(math.log(operand))
                    elif token == 'sqrt':
                        if operand < 0:
                            raise ValueError("Square root undefined for negative values.")
                        stack.append(math.sqrt(operand))
                    elif token == 'exp':
                        stack.append(math.exp(operand))
                    elif token == 'abs':
                        stack.append(abs(operand))
                    elif token == 'sqr':
                        stack.append(operand ** 2)
                    elif token == 'arctan':
                        stack.append(math.atan(operand))
                    else:
                        raise ValueError(f"Unknown function '{token}'.")
                except Exception as e:
                    raise ValueError(f"Error evaluating function '{token}': {e}")
            elif isinstance(token, str) and token.isidentifier():
                if token not in symbol_table or symbol_table[token] is None:
                    value = float(input(f"Enter value for variable '{token}': "))
                    symbol_table[token] = value
                stack.append(symbol_table[token])
            else:
                raise ValueError(f"Unexpected token '{token}' encountered.")
        except Exception as e:
            print(f"Error processing token '{token}': {e}")
            return None
    
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    
    return stack.pop()

