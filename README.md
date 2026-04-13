# Simple Expression Evaluator

This project is a simple **mathematical expression evaluator** written in Python.
It reads an expression from a file, converts it to postfix form, and then calculates the result.

---

## Features

* Supports basic operations:

  * `+ , - , * , / , ^`
* Supports special operators:

  * `mod` (modulo)
  * `div` (integer division)
* Supports functions:

  * `sin, cos, tan`
  * `log, sqrt, exp`
  * `abs, sqr, arctan`
* Supports variables (user input)
* Handles errors (like division by zero, wrong input, etc.)

---

## Project Structure

* `lexer.py` → breaks input into tokens
* `parser.py` → converts expression to postfix
* `evaluator.py` → calculates the result
* `main.py` → runs the program
* `input.txt` → contains the expression

---

## How to Run

1. Clone the repository:

```bash
git clone <your-repo-link>
cd <repo-folder>
```

2. Make sure you have Python installed.

3. Write your expression in `input.txt`, for example:

```
3 + 4 * 2
```

4. Run the program:

```bash
python main.py
```

---

## Variables

If your expression has variables like:

```
a + b * 2
```

The program will ask you to enter values for `a` and `b`.

---

## Notes

* Trigonometric functions use **degrees**, not radians.
* `log` only works for positive numbers.
* `sqrt` only works for non-negative numbers.
* Division by zero is not allowed.

---

## Example

**input.txt**

```
5 + 3 * 2
```

**Output**

```
Result: 11
```

---

## Goal of Project

This project was created to practice:

* Lexical analysis (Lexer)
* Parsing expressions
* Stack-based evaluation (Postfix)

---

## Author

Created as a beginner-friendly project for learning compilers and expression evaluation.
