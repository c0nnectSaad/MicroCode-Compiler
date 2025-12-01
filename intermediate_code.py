"""
Intermediate Code Generator (Phase 4)
Generates three-address code (TAC) from AST.
"""

from typing import List, Optional
from parser import ASTNode, Program, Declaration, Assignment, PrintStmt, IfStmt, WhileStmt, \
    ForStmt, PatternStmt, BinaryOp, UnaryOp, Identifier, Integer, String


class TACInstruction:
    """Three-Address Code instruction"""
    def __init__(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None, result: Optional[str] = None):
        self.op = op  # Operation
        self.arg1 = arg1  # First operand
        self.arg2 = arg2  # Second operand
        self.result = result  # Result variable
    
    def __repr__(self):
        if self.arg2 is not None:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.arg1 is not None:
            return f"{self.result} = {self.op} {self.arg1}"
        elif self.result is not None:
            return f"{self.result} = {self.op}"
        else:
            return self.op


class IntermediateCodeGenerator:
    """
    Generates three-address code (TAC) from AST.
    Creates intermediate representation suitable for optimization and code generation.
    """
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def generate(self, ast: Program) -> List[TACInstruction]:
        """Generate TAC from AST"""
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
        self.visit_program(ast)
        return self.instructions
    
    def new_temp(self) -> str:
        """Generate new temporary variable name"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self) -> str:
        """Generate new label name"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None, 
             result: Optional[str] = None):
        """Emit a TAC instruction"""
        self.instructions.append(TACInstruction(op, arg1, arg2, result))
    
    def visit_program(self, node: Program):
        """Visit program node"""
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node: ASTNode):
        """Visit statement nodes"""
        if isinstance(node, Declaration):
            self.visit_declaration(node)
        elif isinstance(node, Assignment):
            self.visit_assignment(node)
        elif isinstance(node, PrintStmt):
            self.visit_print(node)
        elif isinstance(node, IfStmt):
            self.visit_if(node)
        elif isinstance(node, WhileStmt):
            self.visit_while(node)
        elif isinstance(node, ForStmt):
            self.visit_for(node)
        elif isinstance(node, PatternStmt):
            self.visit_pattern(node)
    
    def visit_declaration(self, node: Declaration):
        """Visit declaration: var identifier = expression;"""
        result = self.visit_expression(node.expression)
        self.emit('=', result, None, node.identifier)
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment: identifier = expression;"""
        result = self.visit_expression(node.expression)
        self.emit('=', result, None, node.identifier)
    
    def visit_print(self, node: PrintStmt):
        """Visit print statement"""
        value = self.visit_expression(node.expression)
        self.emit('print', value, None, None)
    
    def visit_if(self, node: IfStmt):
        """Visit if statement"""
        condition_temp = self.visit_expression(node.condition)
        else_label = self.new_label()
        end_label = self.new_label()
        
        # Jump to else if condition is false
        self.emit('if_false', condition_temp, else_label if node.else_block else end_label, None)
        
        # Then block
        for stmt in node.then_block:
            self.visit_statement(stmt)
        
        if node.else_block:
            self.emit('goto', end_label, None, None)
            self.emit('label', else_label, None, None)
            # Else block
            for stmt in node.else_block:
                self.visit_statement(stmt)
        
        self.emit('label', end_label, None, None)
    
    def visit_while(self, node: WhileStmt):
        """Visit while statement"""
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('label', start_label, None, None)
        condition_temp = self.visit_expression(node.condition)
        self.emit('if_false', condition_temp, end_label, None)
        
        # Loop body
        for stmt in node.block:
            self.visit_statement(stmt)
        
        self.emit('goto', start_label, None, None)
        self.emit('label', end_label, None, None)
    
    def visit_for(self, node: ForStmt):
        """Visit for statement"""
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Initialize
        self.visit_assignment(node.init)
        
        self.emit('label', start_label, None, None)
        condition_temp = self.visit_expression(node.condition)
        self.emit('if_false', condition_temp, end_label, None)
        
        # Loop body
        for stmt in node.block:
            self.visit_statement(stmt)
        
        # Update
        self.visit_assignment(node.update)
        self.emit('goto', start_label, None, None)
        self.emit('label', end_label, None, None)
    
    def visit_pattern(self, node: PatternStmt):
        """Visit pattern statement"""
        # node.args contains the actual arguments (not the identifier)
        # node.identifier is the result variable name
        args = [self.visit_expression(arg) for arg in node.args]
        self.emit(node.pattern_type, ','.join(args), None, node.identifier)
    
    def visit_expression(self, node: ASTNode) -> str:
        """Visit expression and return temporary variable name"""
        if isinstance(node, Identifier):
            return node.name
        elif isinstance(node, Integer):
            return str(node.value)
        elif isinstance(node, String):
            return f'"{node.value}"'
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        else:
            return "unknown"
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """Visit binary operation"""
        left = self.visit_expression(node.left)
        right = self.visit_expression(node.right)
        temp = self.new_temp()
        
        # Map operators to TAC operations
        op_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            '%': 'mod',
            '==': 'eq',
            '!=': 'ne',
            '<': 'lt',
            '>': 'gt',
            '<=': 'le',
            '>=': 'ge'
        }
        
        tac_op = op_map.get(node.op, node.op)
        self.emit(tac_op, left, right, temp)
        return temp
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """Visit unary operation"""
        operand = self.visit_expression(node.operand)
        temp = self.new_temp()
        
        if node.op == '-':
            self.emit('neg', operand, None, temp)
        else:
            self.emit(node.op, operand, None, temp)
        
        return temp

