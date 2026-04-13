import math
from lexer import Lexer
from parser import Parser
from evaluator import evaluate

def get_variable_values(variable_values):
    for var in variable_values:
        if variable_values[var] is None:
            try:
                value = float(input(f"\n{var}: "))
                variable_values[var] = value
            except ValueError:
                print(f"Invalid input for variable {var}. Please enter a numeric value.")
                return False
    return True

def main():
    try:
        with open('input.txt', 'r') as f:
            input_data = f.read()  
    except FileNotFoundError:
        print("Error: The file 'input.txt' was not found.")
        return
    except IOError:
        print("Error: An error occurred while reading the file.")
        return

    lexer = Lexer(input_data)
    print('\nPostfix: ')
    parser = Parser(lexer)

    try:
        postfix_str = parser.parse()
    except ValueError as e:
        print("Error during parsing:", e)
        return  
    except SyntaxError as e:
        print("Syntax Error during parsing:", e)
        return  

    if lexer.variable_values:
        if not get_variable_values(lexer.variable_values):
            return  

        if any(value is None for value in lexer.variable_values.values()):
            print("Error: All variables must have assigned values.")
            return

    symbol_table_values = {k: float(v) for k, v in lexer.variable_values.items()}

    if postfix_str:
        try:
            result = evaluate(postfix_str, symbol_table_values)
            print(f"\n\nResult: {int(result)}")
        except (SyntaxError, ZeroDivisionError, ValueError, TypeError) as e:
            print("Error during evaluation:", e)
    else:
        print("Error: Postfix expression not defined.")
        
if __name__ == "__main__":
    main()
