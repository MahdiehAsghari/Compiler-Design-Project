class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.peek = 0
        self.line_number = 1
        self.open_parentheses_count = 0
        self.constants = {
            'pi': 3.141592653589793,
            'e': 2.718281828459045,
        }
        self.functions = {
            'sqrt': 'sqrt',
            'sqr': 'sqr',
            'exp': 'exp',
            'sin': 'sin',
            'cos': 'cos',
            'tan': 'tan',
            'cotan': 'cotan',
            'arcsin': 'arcsin',
            'arctan': 'arctan',
            'arccos': 'arccos',
            'arccotan': 'arccotan',
            'log': 'log',
        }
        self.variable_values = {}  

    def parse_number(self):
        number = 0
        has_decimal = False
        has_exponent = False
        fractional_part = 0.0
        fractional_divisor = 10.0
        exponent = 0
        exponent_sign = 1

        while self.peek < len(self.input_string):
            char = self.input_string[self.peek]

            if char.isdigit():
                if not has_decimal and not has_exponent:
                    number = number * 10 + int(char)
                elif has_decimal and not has_exponent:
                    fractional_part += int(char) / fractional_divisor
                    fractional_divisor *= 10.0
                elif has_exponent:
                    exponent = exponent * 10 + int(char)
            elif char == '.' and not has_decimal and not has_exponent:
                has_decimal = True
            elif char.lower() == 'e' and not has_exponent:
                has_exponent = True
            elif char in ['+', '-'] and has_exponent and exponent == 0:
                exponent_sign = 1 if char == '+' else -1
            else:
                break

            self.peek += 1

        result = number + fractional_part
        if has_exponent:
            result *= 10 ** (exponent_sign * exponent)

        if result.is_integer():
            result = int(result)

        return ('NUMBER', result)

    def scan(self):
        while self.peek < len(self.input_string):
            char = self.input_string[self.peek]

            while char in [' ', '\t', '\n']:
                if char == '\n':
                    self.line_number += 1
                self.peek += 1
                if self.peek < len(self.input_string):
                    char = self.input_string[self.peek]
                else:
                    return None

            if char == '/' and self.peek + 1 < len(self.input_string) and self.input_string[self.peek + 1] == '/':
                while self.peek < len(self.input_string) and self.input_string[self.peek] != '\n':
                    self.peek += 1
                continue

            if char == '{':
                while self.peek < len(self.input_string) and self.input_string[self.peek] != '}':
                    if self.input_string[self.peek] == '\n':
                        self.line_number += 1
                    self.peek += 1
                if self.peek >= len(self.input_string):
                    raise ValueError(f"Unmatched opening '{{' at line {self.line_number}")
                self.peek += 1
                continue

            if char == '}':
                has_matching_open = False
                for i in range(self.peek - 1, -1, -1):
                    if self.input_string[i] == '{':
                        has_matching_open = True
                        break
                if not has_matching_open:
                    raise ValueError(f"Unmatched closing '}}' at line {self.line_number}")
                self.peek += 1
                continue

            if char.isdigit() or char == '.':
                if self.input_string[self.peek+1].isalpha(): 
                    raise SyntaxError(f"\nERROR: Invalid identifier starting with a digit at line {self.line_number}")
                return self.parse_number()

            if char == '-':
                self.peek += 1
                return ('OPERATOR', '-')

            if self.input_string[self.peek:self.peek + 3] in ['mod', 'div']:
                operator = self.input_string[self.peek:self.peek + 3]
                self.peek += 3
                return ('OPERATOR', operator)

            if char in ['+', '*', '/', '^']:
                self.peek += 1
                return ('OPERATOR', char)

            if char == '(':
                self.open_parentheses_count += 1
                self.peek += 1
                return ('PARENTHESIS', '(')

            elif char == ')':
                self.open_parentheses_count -= 1
                if self.open_parentheses_count < 0:
                    raise ValueError(f"Unmatched closing parenthesis at line {self.line_number}")
                self.peek += 1
                return ('PARENTHESIS', ')')

            if char.isalpha() or char == '_':
                func_name = ''
                if char.isalpha() or char == '_': 
                    func_name += char
                    self.peek += 1
                    while self.peek < len(self.input_string) and (self.input_string[self.peek].isalnum() or self.input_string[self.peek] == '_'):
                        func_name += self.input_string[self.peek]
                        self.peek += 1

                if func_name.lower() in self.constants:
                    return ('CONSTANT', func_name.lower())
                elif func_name.lower() in self.functions:
                    return ('FUNCTION', self.functions[func_name.lower()])
                else:
                    if func_name[0].isdigit():
                        raise ValueError(f"Invalid identifier '{func_name}' starting with a digit at line {self.line_number}")
                    if func_name.lower() not in self.variable_values:
                        self.variable_values[func_name.lower()] = None
                    return ('IDENTIFIER', func_name.lower())

            raise ValueError(f"Unrecognized character '{char}' at line {self.line_number}")

        if self.open_parentheses_count > 0:
            raise ValueError(f"Unmatched opening parenthesis at line {self.line_number}")

        return None
