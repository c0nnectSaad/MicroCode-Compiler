"""
Optimizer (Phase 5)
Performs basic optimizations: constant folding, dead code elimination.
"""

from intermediate_code import TACInstruction, IntermediateCodeGenerator
from typing import List, Set, Optional


class Optimizer:
    """
    Optimizer performing basic optimizations on three-address code.
    Implements constant folding and dead code elimination.
    """
    
    def __init__(self):
        self.constants: dict = {}  # Track constant values
        self.used_vars: Set[str] = set()  # Track used variables
    
    def optimize(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Apply optimizations to TAC instructions.
        Returns optimized instruction list.
        """
        optimized = []
        
        # First pass: constant folding
        optimized = self.constant_folding(instructions)
        
        # Second pass: dead code elimination
        optimized = self.dead_code_elimination(optimized)
        
        return optimized
    
    def constant_folding(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """Fold constant expressions at compile time"""
        optimized = []
        self.constants = {}
        
        for instr in instructions:
            # Skip labels and control flow
            if instr.op in ('label', 'goto', 'if_false', 'print'):
                optimized.append(instr)
                continue
            
            # Constant folding for arithmetic operations
            if instr.op in ('add', 'sub', 'mul', 'div', 'mod'):
                result = self.fold_arithmetic(instr)
                if result is not None:
                    self.constants[instr.result] = result
                    # Replace with constant assignment
                    optimized.append(TACInstruction('=', str(result), None, instr.result))
                else:
                    optimized.append(instr)
            
            # Constant folding for comparison operations
            elif instr.op in ('eq', 'ne', 'lt', 'gt', 'le', 'ge'):
                result = self.fold_comparison(instr)
                if result is not None:
                    self.constants[instr.result] = result
                    optimized.append(TACInstruction('=', str(result), None, instr.result))
                else:
                    optimized.append(instr)
            
            # Constant propagation for assignments
            elif instr.op == '=':
                # If assigning a constant, track it
                if self.is_constant(instr.arg1):
                    value = self.get_constant_value(instr.arg1)
                    self.constants[instr.result] = value
                    optimized.append(instr)
                else:
                    # Variable assignment - remove from constants if it was constant
                    if instr.result in self.constants:
                        del self.constants[instr.result]
                    optimized.append(instr)
            
            # Unary operations
            elif instr.op == 'neg':
                result = self.fold_unary(instr)
                if result is not None:
                    self.constants[instr.result] = result
                    optimized.append(TACInstruction('=', str(result), None, instr.result))
                else:
                    optimized.append(instr)
            
            else:
                optimized.append(instr)
        
        return optimized
    
    def fold_arithmetic(self, instr: TACInstruction) -> Optional[int]:
        """Fold arithmetic operation if both operands are constants"""
        arg1_val = self.get_constant_value(instr.arg1)
        arg2_val = self.get_constant_value(instr.arg2)
        
        if arg1_val is None or arg2_val is None:
            return None
        
        try:
            if instr.op == 'add':
                return arg1_val + arg2_val
            elif instr.op == 'sub':
                return arg1_val - arg2_val
            elif instr.op == 'mul':
                return arg1_val * arg2_val
            elif instr.op == 'div':
                if arg2_val == 0:
                    return None  # Division by zero
                return arg1_val // arg2_val
            elif instr.op == 'mod':
                if arg2_val == 0:
                    return None
                return arg1_val % arg2_val
        except:
            return None
        
        return None
    
    def fold_comparison(self, instr: TACInstruction) -> Optional[int]:
        """Fold comparison operation if both operands are constants"""
        arg1_val = self.get_constant_value(instr.arg1)
        arg2_val = self.get_constant_value(instr.arg2)
        
        if arg1_val is None or arg2_val is None:
            return None
        
        if instr.op == 'eq':
            return 1 if arg1_val == arg2_val else 0
        elif instr.op == 'ne':
            return 1 if arg1_val != arg2_val else 0
        elif instr.op == 'lt':
            return 1 if arg1_val < arg2_val else 0
        elif instr.op == 'gt':
            return 1 if arg1_val > arg2_val else 0
        elif instr.op == 'le':
            return 1 if arg1_val <= arg2_val else 0
        elif instr.op == 'ge':
            return 1 if arg1_val >= arg2_val else 0
        
        return None
    
    def fold_unary(self, instr: TACInstruction) -> Optional[int]:
        """Fold unary operation if operand is constant"""
        arg_val = self.get_constant_value(instr.arg1)
        
        if arg_val is None:
            return None
        
        if instr.op == 'neg':
            return -arg_val
        
        return None
    
    def is_constant(self, value: str) -> bool:
        """Check if value is a constant"""
        if value is None:
            return False
        # Check if it's a numeric string
        try:
            int(value)
            return True
        except ValueError:
            # Check if it's in constants dictionary
            return value in self.constants
    
    def get_constant_value(self, value: str) -> Optional[int]:
        """Get constant value"""
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return self.constants.get(value)
    
    def dead_code_elimination(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """Eliminate dead code (unused assignments)"""
        # Find all used variables
        self.used_vars = set()
        
        # Backward pass to find used variables
        for instr in reversed(instructions):
            if instr.op == 'print':
                if instr.arg1:
                    self.used_vars.add(instr.arg1)
            elif instr.op == 'if_false':
                if instr.arg1:
                    self.used_vars.add(instr.arg1)
            elif instr.op in ('fibonacci', 'factorial', 'sequence'):
                # Pattern functions: mark result and arguments as used
                if instr.result:
                    self.used_vars.add(instr.result)
                if instr.arg1:
                    # Arguments are comma-separated
                    args = instr.arg1.split(',')
                    for arg in args:
                        arg = arg.strip()
                        # Add argument to used_vars if it's not a constant
                        if arg:
                            try:
                                int(arg)  # If it's a number, skip it
                            except ValueError:
                                self.used_vars.add(arg)
            elif instr.op in ('add', 'sub', 'mul', 'div', 'mod', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'neg'):
                if instr.arg1:
                    self.used_vars.add(instr.arg1)
                if instr.arg2:
                    self.used_vars.add(instr.arg2)
                if instr.result and instr.result in self.used_vars:
                    # Result is used, so operands are used
                    pass
            elif instr.op == '=':
                # If result is used, mark it
                if instr.result in self.used_vars:
                    if instr.arg1:
                        self.used_vars.add(instr.arg1)
        
        # Forward pass: eliminate unused assignments
        optimized = []
        for instr in instructions:
            # Keep control flow, labels, and print statements
            if instr.op in ('label', 'goto', 'if_false', 'print', 'fibonacci', 'factorial', 'sequence'):
                optimized.append(instr)
            # Keep assignments if result is used
            elif instr.op == '=':
                if instr.result in self.used_vars or instr.result.startswith('t'):
                    # Keep temp variables and used variables
                    optimized.append(instr)
            # Keep other operations if result might be used
            elif instr.result in self.used_vars:
                optimized.append(instr)
            # Eliminate unused operations
            # (In practice, we keep them for safety, but mark as eliminated)
        
        return optimized

