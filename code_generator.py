"""
Code Generator (Phase 6)
Generates executable code from optimized TAC.
Implements an interpreter that executes TAC instructions.
"""

from typing import Dict, List, Any
from intermediate_code import TACInstruction


class CodeGenerator:
    """
    Code Generator that executes three-address code.
    Acts as an interpreter for the generated intermediate code.
    """
    
    def __init__(self):
        self.memory: Dict[str, Any] = {}  # Variable storage
        self.output: List[str] = []  # Output buffer
        self.pc = 0  # Program counter
        self.labels: Dict[str, int] = {}  # Label to instruction index mapping
    
    def generate(self, instructions: List[TACInstruction]) -> List[str]:
        """
        Execute TAC instructions and return output.
        This is the final code generation phase.
        """
        self.memory = {}
        self.output = []
        self.pc = 0
        self.labels = {}
        
        # First pass: build label map
        for i, instr in enumerate(instructions):
            if instr.op == 'label':
                self.labels[instr.arg1] = i
        
        # Second pass: execute instructions
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.execute_instruction(instr)
            self.pc += 1
        
        return self.output
    
    def execute_instruction(self, instr: TACInstruction):
        """Execute a single TAC instruction"""
        if instr.op == '=':
            # Assignment
            value = self.get_value(instr.arg1)
            self.memory[instr.result] = value
        
        elif instr.op == 'add':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = arg1 + arg2
        
        elif instr.op == 'sub':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = arg1 - arg2
        
        elif instr.op == 'mul':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = arg1 * arg2
        
        elif instr.op == 'div':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            if arg2 == 0:
                raise RuntimeError("Division by zero")
            self.memory[instr.result] = arg1 // arg2
        
        elif instr.op == 'mod':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            if arg2 == 0:
                raise RuntimeError("Modulo by zero")
            self.memory[instr.result] = arg1 % arg2
        
        elif instr.op == 'neg':
            arg1 = self.get_value(instr.arg1)
            self.memory[instr.result] = -arg1
        
        elif instr.op == 'eq':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = 1 if arg1 == arg2 else 0
        
        elif instr.op == 'ne':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = 1 if arg1 != arg2 else 0
        
        elif instr.op == 'lt':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = 1 if arg1 < arg2 else 0
        
        elif instr.op == 'gt':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = 1 if arg1 > arg2 else 0
        
        elif instr.op == 'le':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = 1 if arg1 <= arg2 else 0
        
        elif instr.op == 'ge':
            arg1 = self.get_value(instr.arg1)
            arg2 = self.get_value(instr.arg2)
            self.memory[instr.result] = 1 if arg1 >= arg2 else 0
        
        elif instr.op == 'print':
            value = self.get_value(instr.arg1)
            self.output.append(str(value))
            print(value)  # Also print to console
        
        elif instr.op == 'label':
            # Label - no operation, just a marker
            pass
        
        elif instr.op == 'goto':
            # Jump to label
            if instr.arg1 in self.labels:
                self.pc = self.labels[instr.arg1]
            else:
                raise RuntimeError(f"Label '{instr.arg1}' not found")
        
        elif instr.op == 'if_false':
            # Conditional jump
            condition = self.get_value(instr.arg1)
            if condition == 0:  # False
                if instr.arg2 in self.labels:
                    self.pc = self.labels[instr.arg2]
                else:
                    raise RuntimeError(f"Label '{instr.arg2}' not found")
        
        elif instr.op == 'fibonacci':
            # Generate Fibonacci sequence
            # Format: fibonacci(var, n) -> args = "n", result = var
            args = instr.arg1.split(',')
            if len(args) >= 1:
                n = int(self.get_value(args[0].strip()))
                result = self.compute_fibonacci(n)
                self.memory[instr.result] = result
            else:
                raise RuntimeError("fibonacci requires 1 argument")
        
        elif instr.op == 'factorial':
            # Compute factorial
            # Format: factorial(var, n) -> args = "n", result = var
            args = instr.arg1.split(',')
            if len(args) >= 1:
                n = int(self.get_value(args[0].strip()))
                result = self.compute_factorial(n)
                self.memory[instr.result] = result
            else:
                raise RuntimeError("factorial requires 1 argument")
        
        elif instr.op == 'sequence':
            # Generate arithmetic sequence
            # Format: sequence(var, start, step) -> args = "start,step", result = var
            args = instr.arg1.split(',')
            if len(args) >= 2:
                start = int(self.get_value(args[0].strip()))
                step = int(self.get_value(args[1].strip()))
                result = self.compute_sequence(start, step)
                self.memory[instr.result] = result
            else:
                raise RuntimeError("sequence requires 2 arguments")
    
    def get_value(self, identifier: str) -> Any:
        """Get value of identifier (variable or constant)"""
        if identifier is None:
            return None
        
        # Try to parse as integer
        try:
            return int(identifier)
        except ValueError:
            pass
        
        # Try to parse as string literal
        if identifier.startswith('"') and identifier.endswith('"'):
            return identifier[1:-1]
        
        # Look up in memory
        if identifier in self.memory:
            return self.memory[identifier]
        
        # Return as-is if not found
        return identifier
    
    def compute_fibonacci(self, n: int) -> List[int]:
        """Compute Fibonacci sequence"""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
    
    def compute_factorial(self, n: int) -> int:
        """Compute factorial"""
        if n < 0:
            return 0
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def compute_sequence(self, start: int, step: int, count: int = 10) -> List[int]:
        """Compute arithmetic sequence"""
        sequence = []
        for i in range(count):
            sequence.append(start + i * step)
        return sequence

