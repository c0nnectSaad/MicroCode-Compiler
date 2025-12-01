"""
Lexical Analyzer (Phase 1)
Tokenizes input source code into tokens using DFA-based recognition.
"""

import re
from enum import Enum
from typing import List, Tuple, Optional


class TokenType(Enum):
    # Keywords
    VAR = 'VAR'
    PRINT = 'PRINT'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    FOR = 'FOR'
    FIBONACCI = 'FIBONACCI'
    FACTORIAL = 'FACTORIAL'
    SEQUENCE = 'SEQUENCE'
    END = 'END'
    
    # Identifiers and Literals
    IDENTIFIER = 'IDENTIFIER'
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    
    # Operators
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'
    ASSIGN = 'ASSIGN'
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS = 'LESS'
    GREATER = 'GREATER'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER_EQUAL = 'GREATER_EQUAL'
    
    # Delimiters
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    COMMA = 'COMMA'
    SEMICOLON = 'SEMICOLON'
    
    # Special
    EOF = 'EOF'
    COMMENT = 'COMMENT'


class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"


class Lexer:
    """
    Lexical Analyzer implementing DFA-based token recognition.
    Uses regular expressions to match tokens according to language specification.
    """
    
    # Keyword mapping
    KEYWORDS = {
        'var': TokenType.VAR,
        'print': TokenType.PRINT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'fibonacci': TokenType.FIBONACCI,
        'factorial': TokenType.FACTORIAL,
        'sequence': TokenType.SEQUENCE,
        'end': TokenType.END,
    }
    
    # Token patterns (regex) - ordered by priority
    TOKEN_PATTERNS = [
        (r'//.*', TokenType.COMMENT),  # Comments first
        (r'\s+', None),  # Whitespace (ignored)
        (r'"[^"]*"', TokenType.STRING),  # String literals
        (r'-?\d+', TokenType.INTEGER),  # Integers
        (r'[a-zA-Z][a-zA-Z0-9_]*', TokenType.IDENTIFIER),  # Identifiers
        (r'==', TokenType.EQUAL),
        (r'!=', TokenType.NOT_EQUAL),
        (r'<=', TokenType.LESS_EQUAL),
        (r'>=', TokenType.GREATER_EQUAL),
        (r'=', TokenType.ASSIGN),
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MULTIPLY),
        (r'/', TokenType.DIVIDE),
        (r'%', TokenType.MODULO),
        (r'<', TokenType.LESS),
        (r'>', TokenType.GREATER),
        (r'\(', TokenType.LPAREN),
        (r'\)', TokenType.RPAREN),
        (r'\{', TokenType.LBRACE),
        (r'\}', TokenType.RBRACE),
        (r',', TokenType.COMMA),
        (r';', TokenType.SEMICOLON),
    ]
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        """Report lexical error"""
        raise SyntaxError(f"Lexical error at line {self.line}, column {self.column}: {message}")
    
    def advance(self, n: int = 1):
        """Advance position and update line/column"""
        for _ in range(n):
            if self.pos < len(self.source) and self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def peek(self, n: int = 0) -> Optional[str]:
        """Peek at character n positions ahead"""
        pos = self.pos + n
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def tokenize(self) -> List[Token]:
        """
        Main tokenization method - implements DFA-based recognition.
        Scans source code and generates tokens according to lexical rules.
        """
        while self.pos < len(self.source):
            matched = False
            
            # Try to match each pattern
            for pattern, token_type in self.TOKEN_PATTERNS:
                regex = re.compile(f'^{pattern}')
                match = regex.match(self.source[self.pos:])
                
                if match:
                    matched = True
                    value = match.group(0)
                    start_line = self.line
                    start_col = self.column
                    
                    # Skip comments and whitespace
                    if token_type is None or token_type == TokenType.COMMENT:
                        self.advance(len(value))
                        break
                    
                    # Check if identifier is a keyword
                    if token_type == TokenType.IDENTIFIER and value.lower() in self.KEYWORDS:
                        token_type = self.KEYWORDS[value.lower()]
                    
                    # Create token
                    token = Token(token_type, value, start_line, start_col)
                    self.tokens.append(token)
                    
                    self.advance(len(value))
                    break
            
            if not matched:
                self.error(f"Unexpected character: '{self.peek()}'")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def get_tokens(self) -> List[Token]:
        """Get tokenized result"""
        if not self.tokens:
            return self.tokenize()
        return self.tokens

