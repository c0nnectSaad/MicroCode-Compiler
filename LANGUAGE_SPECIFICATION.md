# PatternScript Language Specification

## Overview
PatternScript is a domain-specific mini language designed for numerical pattern generation. It supports arithmetic sequences, Fibonacci-like patterns, factorial calculations, and custom mathematical operations.

## Lexical Rules

### Tokens
1. **Keywords**: `var`, `print`, `if`, `else`, `while`, `for`, `fibonacci`, `factorial`, `sequence`, `end`
2. **Identifiers**: Start with letter, followed by letters/digits/underscores (e.g., `x`, `counter`, `my_var`)
3. **Literals**: 
   - Integers: `0`, `123`, `-45`
   - Strings: `"hello"`, `"pattern"`
4. **Operators**: `+`, `-`, `*`, `/`, `%`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`
5. **Delimiters**: `(`, `)`, `{`, `}`, `,`, `;`
6. **Comments**: `//` single-line comments

### Regular Expressions
- Identifier: `[a-zA-Z][a-zA-Z0-9_]*`
- Integer: `-?[0-9]+`
- String: `"[^"]*"`
- Whitespace: `[ \t\n\r]+` (ignored)

## Syntax (BNF Grammar)

```
program ::= statement_list

statement_list ::= statement | statement_list statement

statement ::= declaration
            | assignment
            | print_stmt
            | if_stmt
            | while_stmt
            | for_stmt
            | pattern_stmt

declaration ::= 'var' identifier '=' expression ';'

assignment ::= identifier '=' expression ';'

print_stmt ::= 'print' expression ';'

if_stmt ::= 'if' '(' condition ')' '{' statement_list '}' 
          | 'if' '(' condition ')' '{' statement_list '}' 'else' '{' statement_list '}'

while_stmt ::= 'while' '(' condition ')' '{' statement_list '}'

for_stmt ::= 'for' '(' identifier '=' expression ';' condition ';' assignment ')' '{' statement_list '}'

pattern_stmt ::= 'fibonacci' '(' identifier ',' expression ')' ';'
               | 'factorial' '(' identifier ',' expression ')' ';'
               | 'sequence' '(' identifier ',' expression ',' expression ')' ';'

expression ::= term | expression '+' term | expression '-' term

term ::= factor | term '*' factor | term '/' factor | term '%' factor

factor ::= integer
         | identifier
         | string
         | '(' expression ')'
         | '-' factor

condition ::= expression '==' expression
            | expression '!=' expression
            | expression '<' expression
            | expression '>' expression
            | expression '<=' expression
            | expression '>=' expression
```

## Semantic Rules

1. **Type System**: 
   - Integer type for numbers
   - String type for text literals
   - Variables must be declared before use
   - Type checking: arithmetic operations require integer operands

2. **Scope Rules**:
   - Global scope for all variables
   - Variables must be initialized when declared

3. **Pattern Functions**:
   - `fibonacci(var, n)`: Generates first n Fibonacci numbers, stores in var
   - `factorial(var, n)`: Calculates factorial of n, stores in var
   - `sequence(var, start, step)`: Generates arithmetic sequence starting at start with step size

## Example Programs

### Example 1: Fibonacci Sequence
```
var n = 10;
fibonacci(result, n);
print result;
```

### Example 2: Factorial Calculation
```
var num = 5;
factorial(fact, num);
print fact;
```

### Example 3: Arithmetic Sequence
```
var start = 2;
var step = 3;
sequence(seq, start, step);
print seq;
```

### Example 4: Loop with Conditionals
```
var i = 0;
while (i < 5) {
    print i;
    i = i + 1;
}
```

