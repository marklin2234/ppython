# PPython

## How to use
1. clone git repository to your local directory
2. Run
```
python3 ppython.py
```
to use it in the terminal.

## How it works
The Lexer tokenizes user input, and stores it in an array. The tokens are passed into the parser, which converts the token array into an abstract syntax tree. This lets the interpreter know the order to execute the current line.

Variables can be declared using:
```
my_variable = 10
```
and are simply stored in a variable table locally. Typing is handled under the hood.

Currently, only basic arithmetic is supported.
For example,
```
> a = 10
> (13 + a) * (2 - a)
-184
```
