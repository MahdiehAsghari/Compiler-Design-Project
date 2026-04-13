class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.scan()
        self.postfix = []
        self.previous_token = None

    def match(self, expected_type, expected_value=None):
        if expected_value is None or (self.current_token and self.current_token[1] == expected_value):
            self.previous_token = self.current_token
            self.current_token = self.lexer.scan()
        else:
            expected = expected_value if expected_value else expected_type
            found = self.current_token[1] if self.current_token else 'None'
            raise SyntaxError(f"Expected {expected} but found {found}")

    def expr(self):
        self.term()
        self.expr_prime()

    def expr_prime(self):
        while self.current_token and self.current_token[1] in ['+', '-']:
            operator = self.current_token[1]
            if self.previous_token and self.previous_token[1] in ['+', '-', '*', '/', 'mod', 'div']: 
                raise SyntaxError(f"\nUnexpected consecutive operators at line {self.lexer.line_number}")
            self.match('OPERATOR', operator)
            self.term()
            self.postfix.append(operator)
            print(operator, end=' ')

    def term(self):
        self.factor()
        self.term_prime()

    def term_prime(self):
        while self.current_token and self.current_token[1] in ['*', '/', 'mod', 'div']:
            operator = self.current_token[1]
            self.match('OPERATOR', operator)
            self.factor()
            self.postfix.append(operator)
            print(operator, end=' ')

    def factor(self):
        if self.current_token[1] == '-':
            if not self.previous_token or (self.previous_token[0] == 'OPERATOR' or self.previous_token[1] != ')'):
                self.match('OPERATOR', '-')
                self.unary_negative()
            else:
                self.base()
                if self.current_token and self.current_token[1] == '^':
                    self.match('OPERATOR', '^')
                    self.factor()
                    self.postfix.append('^')
                    print('^', end=' ')
        else:
            self.base()
            if self.current_token and self.current_token[1] == '^':
                self.match('OPERATOR', '^')
                self.factor()
                self.postfix.append('^')
                print('^', end=' ')

    def unary_negative(self):
        self.factor()
        self.postfix.append('neg')
        print('neg', end=' ')

    def base(self):
        if self.current_token[1] == '(':
            self.match('PARENTHESIS', '(')
            self.expr()
            self.match('PARENTHESIS', ')')
        elif self.current_token[0] == 'NUMBER':
            print(self.current_token[1], end=' ')
            self.postfix.append(self.current_token[1])
            self.match('NUMBER')
        elif self.current_token[0] == 'IDENTIFIER':
            print(self.current_token[1], end=' ')
            self.postfix.append(self.current_token[1])
            self.match('IDENTIFIER')
        elif self.current_token[0] == 'CONSTANT':
            constant = self.current_token[1] 
            if constant == 'pi': 
                constant = 'pi' 
                self.postfix.append(3.141592653589793)
            elif constant == 'e': 
                constant = 'e'
                self.postfix.append(2.718281828459045)
            print(constant, end=' ')
            
            self.match('CONSTANT')
        elif self.current_token[0] == 'FUNCTION':
            function_name = self.current_token[1]
            self.match('FUNCTION', function_name)
            self.match('PARENTHESIS', '(')
            self.expr()
            self.match('PARENTHESIS', ')')
            self.postfix.append(function_name)
            print(function_name, end=' ')
        else:
            raise SyntaxError("Unexpected token")

    def parse(self):
        self.expr()
        if self.current_token:
            raise SyntaxError(f"Unexpected token at the end of input: {self.current_token}")
        return self.postfix

    def print_postfix(self):
        print("\nPostfix:")
        print(' '.join(map(str, self.postfix)))


