"""
Syntax Analyzer (Phase 2)
Parses tokens according to BNF grammar and builds Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Union
from lexer import Token, TokenType


class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self, token: Optional[Token] = None):
        self.token = token
        self.line = token.line if token else 0
        self.column = token.column if token else 0
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Program(ASTNode):
    """Root node representing entire program"""
    def __init__(self, statements: List[ASTNode]):
        super().__init__()
        self.statements = statements
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


class Declaration(ASTNode):
    """Variable declaration: var identifier = expression;"""
    def __init__(self, identifier: str, expression: ASTNode, token: Token):
        super().__init__(token)
        self.identifier = identifier
        self.expression = expression
    
    def __repr__(self):
        return f"Declaration({self.identifier} = {self.expression})"


class Assignment(ASTNode):
    """Variable assignment: identifier = expression;"""
    def __init__(self, identifier: str, expression: ASTNode, token: Token):
        super().__init__(token)
        self.identifier = identifier
        self.expression = expression
    
    def __repr__(self):
        return f"Assignment({self.identifier} = {self.expression})"


class PrintStmt(ASTNode):
    """Print statement: print expression;"""
    def __init__(self, expression: ASTNode, token: Token):
        super().__init__(token)
        self.expression = expression
    
    def __repr__(self):
        return f"Print({self.expression})"


class IfStmt(ASTNode):
    """If statement: if (condition) { statements } [else { statements }]"""
    def __init__(self, condition: ASTNode, then_block: List[ASTNode], 
                 else_block: Optional[List[ASTNode]], token: Token):
        super().__init__(token)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
    
    def __repr__(self):
        return f"If({self.condition}, then={len(self.then_block)}, else={len(self.else_block) if self.else_block else 0})"


class WhileStmt(ASTNode):
    """While statement: while (condition) { statements }"""
    def __init__(self, condition: ASTNode, block: List[ASTNode], token: Token):
        super().__init__(token)
        self.condition = condition
        self.block = block
    
    def __repr__(self):
        return f"While({self.condition}, {len(self.block)} statements)"


class ForStmt(ASTNode):
    """For statement: for (init; condition; update) { statements }"""
    def __init__(self, init: Assignment, condition: ASTNode, update: Assignment,
                 block: List[ASTNode], token: Token):
        super().__init__(token)
        self.init = init
        self.condition = condition
        self.update = update
        self.block = block
    
    def __repr__(self):
        return f"For({self.init}, {self.condition}, {self.update}, {len(self.block)} statements)"


class PatternStmt(ASTNode):
    """Pattern statement: fibonacci/factorial/sequence(...)"""
    def __init__(self, pattern_type: str, identifier: str, args: List[ASTNode], token: Token):
        super().__init__(token)
        self.pattern_type = pattern_type  # 'fibonacci', 'factorial', 'sequence'
        self.identifier = identifier
        self.args = args
    
    def __repr__(self):
        return f"Pattern({self.pattern_type}, {self.identifier}, args={len(self.args)})"


class BinaryOp(ASTNode):
    """Binary operation: left op right"""
    def __init__(self, left: ASTNode, op: str, right: ASTNode, token: Token):
        super().__init__(token)
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"


class UnaryOp(ASTNode):
    """Unary operation: op operand"""
    def __init__(self, op: str, operand: ASTNode, token: Token):
        super().__init__(token)
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.op} {self.operand})"


class Identifier(ASTNode):
    """Identifier reference"""
    def __init__(self, name: str, token: Token):
        super().__init__(token)
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name})"


class Integer(ASTNode):
    """Integer literal"""
    def __init__(self, value: int, token: Token):
        super().__init__(token)
        self.value = value
    
    def __repr__(self):
        return f"Integer({self.value})"


class String(ASTNode):
    """String literal"""
    def __init__(self, value: str, token: Token):
        super().__init__(token)
        self.value = value
    
    def __repr__(self):
        return f"String('{self.value}')"


class Parser:
    """
    Recursive descent parser implementing BNF grammar rules.
    Builds Abstract Syntax Tree from token stream.
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        """Get current token"""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def peek_token(self, n: int = 1) -> Token:
        """Peek at token n positions ahead"""
        pos = self.pos + n
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[pos]
    
    def consume(self, expected_type: TokenType, error_msg: str = None) -> Token:
        """Consume token of expected type"""
        token = self.current_token()
        if token.type != expected_type:
            msg = error_msg or f"Expected {expected_type.name}, got {token.type.name}"
            raise SyntaxError(f"Syntax error at line {token.line}, column {token.column}: {msg}")
        self.pos += 1
        return token
    
    def error(self, message: str):
        """Report syntax error"""
        token = self.current_token()
        raise SyntaxError(f"Syntax error at line {token.line}, column {token.column}: {message}")
    
    def parse(self) -> Program:
        """Parse program and return AST"""
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement"""
        token = self.current_token()
        
        if token.type == TokenType.VAR:
            return self.parse_declaration()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.WHILE:
            return self.parse_while()
        elif token.type == TokenType.FOR:
            return self.parse_for()
        elif token.type in (TokenType.FIBONACCI, TokenType.FACTORIAL, TokenType.SEQUENCE):
            return self.parse_pattern()
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        elif token.type == TokenType.RBRACE:
            return None  # End of block
        else:
            self.error(f"Unexpected token: {token.type.name}")
    
    def parse_declaration(self) -> Declaration:
        """Parse: var identifier = expression;"""
        var_token = self.consume(TokenType.VAR)
        id_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN, "Expected '=' after identifier")
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after declaration")
        return Declaration(id_token.value, expr, var_token)
    
    def parse_assignment(self) -> Assignment:
        """Parse: identifier = expression;"""
        id_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN, "Expected '=' after identifier")
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        return Assignment(id_token.value, expr, id_token)
    
    def parse_print(self) -> PrintStmt:
        """Parse: print expression;"""
        print_token = self.consume(TokenType.PRINT)
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after print")
        return PrintStmt(expr, print_token)
    
    def parse_if(self) -> IfStmt:
        """Parse: if (condition) { statements } [else { statements }]"""
        if_token = self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        self.consume(TokenType.LBRACE, "Expected '{' after condition")
        
        then_block = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
        self.consume(TokenType.RBRACE)
        
        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.consume(TokenType.ELSE)
            self.consume(TokenType.LBRACE, "Expected '{' after 'else'")
            else_block = []
            while self.current_token().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
            self.consume(TokenType.RBRACE)
        
        return IfStmt(condition, then_block, else_block, if_token)
    
    def parse_while(self) -> WhileStmt:
        """Parse: while (condition) { statements }"""
        while_token = self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        self.consume(TokenType.LBRACE, "Expected '{' after condition")
        
        block = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                block.append(stmt)
        self.consume(TokenType.RBRACE)
        
        return WhileStmt(condition, block, while_token)
    
    def parse_for(self) -> ForStmt:
        """Parse: for (init; condition; update) { statements }"""
        for_token = self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN, "Expected '(' after 'for'")
        
        # Parse init (must be assignment)
        init_id = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN)
        init_expr = self.parse_expression()
        init = Assignment(init_id.value, init_expr, init_id)
        self.consume(TokenType.SEMICOLON)
        
        # Parse condition
        condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        
        # Parse update (must be assignment)
        update_id = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN)
        update_expr = self.parse_expression()
        update = Assignment(update_id.value, update_expr, update_id)
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE, "Expected '{' after for loop")
        
        # Parse block
        block = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                block.append(stmt)
        self.consume(TokenType.RBRACE)
        
        return ForStmt(init, condition, update, block, for_token)
    
    def parse_pattern(self) -> PatternStmt:
        """Parse: fibonacci/factorial/sequence(identifier, args...)"""
        token = self.current_token()
        pattern_type = None
        
        if token.type == TokenType.FIBONACCI:
            self.consume(TokenType.FIBONACCI)
            pattern_type = 'fibonacci'
        elif token.type == TokenType.FACTORIAL:
            self.consume(TokenType.FACTORIAL)
            pattern_type = 'factorial'
        elif token.type == TokenType.SEQUENCE:
            self.consume(TokenType.SEQUENCE)
            pattern_type = 'sequence'
        
        self.consume(TokenType.LPAREN, f"Expected '(' after '{pattern_type}'")
        id_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.COMMA, "Expected ',' after identifier")
        
        args = []
        while True:
            args.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        
        self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        self.consume(TokenType.SEMICOLON, "Expected ';' after pattern statement")
        
        return PatternStmt(pattern_type, id_token.value, args, token)
    
    def parse_expression(self) -> ASTNode:
        """Parse expression (lowest precedence)"""
        return self.parse_equality()
    
    def parse_equality(self) -> ASTNode:
        """Parse equality/inequality expressions"""
        left = self.parse_relational()
        
        while self.current_token().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op_token = self.current_token()
            self.pos += 1
            op = '==' if op_token.type == TokenType.EQUAL else '!='
            right = self.parse_relational()
            left = BinaryOp(left, op, right, op_token)
        
        return left
    
    def parse_relational(self) -> ASTNode:
        """Parse relational expressions"""
        left = self.parse_additive()
        
        while self.current_token().type in (TokenType.LESS, TokenType.GREATER, 
                                            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op_token = self.current_token()
            self.pos += 1
            op_map = {
                TokenType.LESS: '<',
                TokenType.GREATER: '>',
                TokenType.LESS_EQUAL: '<=',
                TokenType.GREATER_EQUAL: '>='
            }
            op = op_map[op_token.type]
            right = self.parse_additive()
            left = BinaryOp(left, op, right, op_token)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse addition/subtraction"""
        left = self.parse_multiplicative()
        
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.pos += 1
            op = '+' if op_token.type == TokenType.PLUS else '-'
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right, op_token)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication/division/modulo"""
        left = self.parse_unary()
        
        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.current_token()
            self.pos += 1
            op_map = {
                TokenType.MULTIPLY: '*',
                TokenType.DIVIDE: '/',
                TokenType.MODULO: '%'
            }
            op = op_map[op_token.type]
            right = self.parse_unary()
            left = BinaryOp(left, op, right, op_token)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary minus"""
        if self.current_token().type == TokenType.MINUS:
            op_token = self.consume(TokenType.MINUS)
            operand = self.parse_unary()
            return UnaryOp('-', operand, op_token)
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions (literals, identifiers, parenthesized)"""
        token = self.current_token()
        
        if token.type == TokenType.INTEGER:
            self.pos += 1
            return Integer(int(token.value), token)
        elif token.type == TokenType.STRING:
            self.pos += 1
            # Remove quotes
            value = token.value[1:-1]
            return String(value, token)
        elif token.type == TokenType.IDENTIFIER:
            self.pos += 1
            return Identifier(token.value, token)
        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        else:
            self.error(f"Unexpected token in expression: {token.type.name}")

