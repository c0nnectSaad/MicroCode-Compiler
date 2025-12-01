# PatternScript Compiler

A complete mini language compiler implementing all six phases of compilation for a domain-specific language designed for numerical pattern generation.

## Language Overview

**PatternScript** is a mini language designed for:
- Numerical pattern generation (Fibonacci, factorial, arithmetic sequences)
- Basic arithmetic operations
- Control flow (if/else, while, for loops)
- Variable declarations and assignments

## Project Structure

```
.
├── compiler.py              # Main compiler orchestrator
├── lexer.py                 # Phase 1: Lexical Analysis
├── parser.py                # Phase 2: Syntax Analysis
├── semantic_analyzer.py     # Phase 3: Semantic Analysis
├── intermediate_code.py     # Phase 4: Intermediate Code Generation
├── optimizer.py              # Phase 5: Optimization
├── code_generator.py         # Phase 6: Code Generation
├── LANGUAGE_SPECIFICATION.md # Complete language specification
├── test_*.ps                # Test case files
└── README.md                # This file
```

## Compilation Phases

### Phase 1: Lexical Analysis
- Tokenizes source code using DFA-based recognition
- Recognizes keywords, identifiers, literals, operators, and delimiters
- Handles comments and whitespace

### Phase 2: Syntax Analysis
- Recursive descent parser implementing BNF grammar
- Builds Abstract Syntax Tree (AST)
- Validates syntax according to language grammar

### Phase 3: Semantic Analysis
- Constructs symbol table with type information
- Performs type checking
- Validates variable declarations and usage
- Ensures variables are initialized before use

### Phase 4: Intermediate Code Generation
- Generates Three-Address Code (TAC)
- Creates intermediate representation suitable for optimization
- Handles control flow with labels and jumps

### Phase 5: Optimization
- Constant folding: evaluates constant expressions at compile time
- Dead code elimination: removes unused assignments
- Basic optimizations to improve code efficiency

### Phase 6: Code Generation
- Executes optimized TAC instructions
- Implements pattern generation functions (Fibonacci, factorial, sequence)
- Produces program output

## Installation

Requires Python 3.7 or higher.

```bash
# No external dependencies required - uses only Python standard library
python3 --version  # Verify Python 3.7+
```

## Usage

### Compile from File

```bash
python compiler.py <source_file> [--verbose]
```

Example:
```bash
python compiler.py test_fibonacci.ps --verbose
```

### Interactive Mode

```bash
python compiler.py --interactive
```

Enter your code line by line, then type `END` on a new line to compile.

### Verbose Mode

Add `--verbose` or `-v` flag to see detailed output from all compilation phases:
- Token list
- Abstract Syntax Tree
- Symbol table
- Three-Address Code (before and after optimization)
- Execution output

## Example Programs

### Example 1: Fibonacci Sequence

```patternscript
var n = 10;
fibonacci(result, n);
print result;
```

**Output:** `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`

### Example 2: Factorial

```patternscript
var num = 5;
factorial(fact, num);
print fact;
```

**Output:** `120`

### Example 3: Arithmetic Sequence with Loop

```patternscript
var start = 2;
var step = 3;
var i = 0;
while (i < 5) {
    var value = start + i * step;
    print value;
    i = i + 1;
}
```

**Output:**
```
2
5
8
11
14
```

### Example 4: Conditional Statements

```patternscript
var a = 10;
var b = 5;
var result = a * b + 2;
print result;

if (result > 50) {
    print "Result is greater than 50";
} else {
    print "Result is less than or equal to 50";
}
```

**Output:**
```
52
Result is greater than 50
```

## Language Syntax

### Variable Declaration
```patternscript
var identifier = expression;
```

### Assignment
```patternscript
identifier = expression;
```

### Print Statement
```patternscript
print expression;
```

### If Statement
```patternscript
if (condition) {
    statements
} else {
    statements
}
```

### While Loop
```patternscript
while (condition) {
    statements
}
```

### For Loop
```patternscript
for (init; condition; update) {
    statements
}
```

### Pattern Functions
```patternscript
fibonacci(identifier, n);      // Generate first n Fibonacci numbers
factorial(identifier, n);      // Calculate factorial of n
sequence(identifier, start, step);  // Generate arithmetic sequence
```

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Assignment: `=`

## Running Test Cases

```bash
# Test Case 1: Fibonacci
python compiler.py test_fibonacci.ps --verbose

# Test Case 2: Factorial
python compiler.py test_factorial.ps --verbose

# Test Case 3: Arithmetic Sequence
python compiler.py test_sequence.ps --verbose

# Test Case 4: Complex Program
python compiler.py test_complex.ps --verbose
```

## Handwritten Artifacts Required

For the project submission, you need to create handwritten documents for:

1. **Lexical Analysis**: DFA/transition table or regex grouping
2. **Syntax Analysis**: At least two parse-tree derivations
3. **Semantic Analysis**: Sample symbol-table fill-in with scope example

These should be scanned/photographed and included in your submission.

## Features

✅ Complete implementation of all 6 compilation phases  
✅ Lexical analysis with DFA-based token recognition  
✅ Syntax analysis with recursive descent parsing  
✅ Semantic analysis with symbol table and type checking  
✅ Intermediate code generation (Three-Address Code)  
✅ Basic optimizations (constant folding, dead code elimination)  
✅ Code generation with pattern function support  
✅ Error handling and reporting  
✅ Verbose mode for debugging  
✅ Interactive mode for testing  

## Limitations

- Single global scope (no nested scopes)
- Integer and String types only
- Basic optimization (more advanced optimizations possible)
- Interpreter-based execution (not native code generation)

## Future Improvements

- Support for arrays and lists
- Function definitions
- Nested scopes
- More advanced optimizations (loop unrolling, register allocation)
- Native code generation
- Better error messages with line/column information

## Author

Compiler Project - PatternScript Implementation

## License

Educational project for compiler construction course.

