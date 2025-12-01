"""
Semantic Analyzer (Phase 3)
Performs type checking and builds symbol table with scope management.
"""

from typing import Dict, Optional, List
from parser import ASTNode, Program, Declaration, Assignment, Identifier, BinaryOp, UnaryOp, Integer, String
from lexer import Token


class SymbolType:
    """Type information for symbols"""
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    UNKNOWN = 'UNKNOWN'


class Symbol:
    """Symbol table entry"""
    def __init__(self, name: str, symbol_type: str, declared: bool = True, initialized: bool = False):
        self.name = name
        self.type = symbol_type
        self.declared = declared
        self.initialized = initialized
        self.line = 0
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.type}, declared={self.declared}, initialized={self.initialized})"


class SymbolTable:
    """Symbol table for variable management"""
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent  # For nested scopes
    
    def declare(self, name: str, symbol_type: str, line: int = 0) -> Symbol:
        """Declare a new symbol"""
        if name in self.symbols:
            raise SemanticError(f"Variable '{name}' already declared at line {line}")
        symbol = Symbol(name, symbol_type, declared=True, initialized=False)
        symbol.line = line
        self.symbols[name] = symbol
        return symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up symbol in current and parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def set_initialized(self, name: str):
        """Mark symbol as initialized"""
        symbol = self.lookup(name)
        if symbol:
            symbol.initialized = True
        else:
            raise SemanticError(f"Variable '{name}' not found")
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Get all symbols including from parent scopes"""
        all_symbols = {}
        if self.parent:
            all_symbols.update(self.parent.get_all_symbols())
        all_symbols.update(self.symbols)
        return all_symbols


class SemanticError(Exception):
    """Semantic analysis error"""
    pass


class SemanticAnalyzer:
    """
    Semantic Analyzer implementing type checking and symbol table management.
    Validates program semantics according to language rules.
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
    
    def analyze(self, ast: Program) -> SymbolTable:
        """
        Perform semantic analysis on AST.
        Returns symbol table with all declared symbols.
        """
        try:
            self.visit_program(ast)
        except SemanticError as e:
            self.errors.append(str(e))
        
        if self.errors:
            raise SemanticError("\n".join(self.errors))
        
        return self.symbol_table
    
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
        elif isinstance(node, Program):
            self.visit_program(node)
        # Other statement types don't need semantic checks beyond their expressions
    
    def visit_declaration(self, node: Declaration):
        """Visit declaration: var identifier = expression;"""
        # Infer type from expression
        expr_type = self.visit_expression(node.expression)
        
        # Declare variable in symbol table
        symbol = self.symbol_table.declare(node.identifier, expr_type, node.line)
        symbol.initialized = True
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment: identifier = expression;"""
        # Check if variable exists
        symbol = self.symbol_table.lookup(node.identifier)
        if not symbol:
            raise SemanticError(f"Variable '{node.identifier}' not declared (line {node.line})")
        
        # Check type compatibility
        expr_type = self.visit_expression(node.expression)
        if symbol.type != expr_type and expr_type != SymbolType.UNKNOWN:
            raise SemanticError(
                f"Type mismatch: '{node.identifier}' is {symbol.type}, "
                f"but expression is {expr_type} (line {node.line})"
            )
        
        symbol.initialized = True
    
    def visit_expression(self, node: ASTNode) -> str:
        """Visit expression and return its type"""
        if isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, Integer):
            return SymbolType.INTEGER
        elif isinstance(node, String):
            return SymbolType.STRING
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        else:
            # For other node types (like pattern statements), return UNKNOWN
            return SymbolType.UNKNOWN
    
    def visit_identifier(self, node: Identifier) -> str:
        """Visit identifier and check if declared"""
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            raise SemanticError(f"Variable '{node.name}' not declared (line {node.line})")
        if not symbol.initialized:
            raise SemanticError(f"Variable '{node.name}' used before initialization (line {node.line})")
        return symbol.type
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """Visit binary operation and check type compatibility"""
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)
        
        # Comparison operators return INTEGER (0 or 1 for false/true)
        if node.op in ('==', '!=', '<', '>', '<=', '>='):
            if left_type != right_type:
                raise SemanticError(
                    f"Type mismatch in comparison: {left_type} {node.op} {right_type} (line {node.line})"
                )
            return SymbolType.INTEGER
        
        # Arithmetic operators require INTEGER operands
        if node.op in ('+', '-', '*', '/', '%'):
            if left_type != SymbolType.INTEGER or right_type != SymbolType.INTEGER:
                raise SemanticError(
                    f"Arithmetic operation requires INTEGER operands, got {left_type} and {right_type} (line {node.line})"
                )
            return SymbolType.INTEGER
        
        return SymbolType.UNKNOWN
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """Visit unary operation"""
        operand_type = self.visit_expression(node.operand)
        if node.op == '-':
            if operand_type != SymbolType.INTEGER:
                raise SemanticError(
                    f"Unary minus requires INTEGER operand, got {operand_type} (line {node.line})"
                )
            return SymbolType.INTEGER
        return operand_type

