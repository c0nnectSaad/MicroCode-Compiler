"""
Main Compiler - Orchestrates all six phases of compilation
"""

import sys
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from intermediate_code import IntermediateCodeGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator


class Compiler:
    """
    Main compiler class that orchestrates all six phases:
    1. Lexical Analysis
    2. Syntax Analysis
    3. Semantic Analysis
    4. Intermediate Code Generation
    5. Optimization
    6. Code Generation
    """
    
    def __init__(self, source: str, verbose: bool = False):
        self.source = source
        self.verbose = verbose
        self.tokens = []
        self.ast = None
        self.symbol_table = None
        self.tac = []
        self.optimized_tac = []
        self.output = []
    
    def compile(self) -> tuple[bool, list[str]]:
        """
        Execute all compilation phases.
        Returns (success, output) tuple.
        """
        try:
            # Phase 1: Lexical Analysis
            if self.verbose:
                print("=" * 60)
                print("PHASE 1: LEXICAL ANALYSIS")
                print("=" * 60)
            
            lexer = Lexer(self.source)
            self.tokens = lexer.tokenize()
            
            if self.verbose:
                print(f"Generated {len(self.tokens)} tokens")
                for token in self.tokens[:20]:  # Show first 20 tokens
                    print(f"  {token}")
                if len(self.tokens) > 20:
                    print(f"  ... and {len(self.tokens) - 20} more tokens")
                print()
            
            # Phase 2: Syntax Analysis
            if self.verbose:
                print("=" * 60)
                print("PHASE 2: SYNTAX ANALYSIS")
                print("=" * 60)
            
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            
            if self.verbose:
                print(f"AST Root: {self.ast}")
                print(f"Number of statements: {len(self.ast.statements)}")
                print()
            
            # Phase 3: Semantic Analysis
            if self.verbose:
                print("=" * 60)
                print("PHASE 3: SEMANTIC ANALYSIS")
                print("=" * 60)
            
            semantic_analyzer = SemanticAnalyzer()
            self.symbol_table = semantic_analyzer.analyze(self.ast)
            
            if self.verbose:
                print("Symbol Table:")
                for name, symbol in self.symbol_table.get_all_symbols().items():
                    print(f"  {name}: {symbol.type} (declared={symbol.declared}, initialized={symbol.initialized})")
                print()
            
            # Phase 4: Intermediate Code Generation
            if self.verbose:
                print("=" * 60)
                print("PHASE 4: INTERMEDIATE CODE GENERATION")
                print("=" * 60)
            
            tac_generator = IntermediateCodeGenerator()
            self.tac = tac_generator.generate(self.ast)
            
            if self.verbose:
                print("Three-Address Code (TAC):")
                for i, instr in enumerate(self.tac):
                    print(f"  {i:3d}: {instr}")
                print()
            
            # Phase 5: Optimization
            if self.verbose:
                print("=" * 60)
                print("PHASE 5: OPTIMIZATION")
                print("=" * 60)
            
            optimizer = Optimizer()
            self.optimized_tac = optimizer.optimize(self.tac)
            
            if self.verbose:
                print("Optimized Three-Address Code:")
                for i, instr in enumerate(self.optimized_tac):
                    print(f"  {i:3d}: {instr}")
                print(f"Reduced from {len(self.tac)} to {len(self.optimized_tac)} instructions")
                print()
            
            # Phase 6: Code Generation
            if self.verbose:
                print("=" * 60)
                print("PHASE 6: CODE GENERATION")
                print("=" * 60)
            
            code_generator = CodeGenerator()
            self.output = code_generator.generate(self.optimized_tac)
            
            if self.verbose:
                print("Execution Output:")
                for line in self.output:
                    print(f"  {line}")
                print()
            
            return True, self.output
        
        except SyntaxError as e:
            if self.verbose:
                print(f"Compilation Error: {e}")
            return False, [f"Syntax Error: {e}"]
        except Exception as e:
            if self.verbose:
                print(f"Runtime Error: {e}")
            return False, [f"Error: {e}"]


def main():
    """Main entry point for command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file> [--verbose]")
        print("   or: python compiler.py --interactive")
        sys.exit(1)
    
    if sys.argv[1] == '--interactive':
        # Interactive mode
        print("PatternScript Compiler - Interactive Mode")
        print("Enter your code (type 'END' on a new line to compile):")
        print("-" * 60)
        
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            except EOFError:
                break
        
        source = '\n'.join(lines)
        verbose = '--verbose' in sys.argv
        
    else:
        # File mode
        source_file = sys.argv[1]
        verbose = '--verbose' in sys.argv or '-v' in sys.argv
        
        try:
            with open(source_file, 'r') as f:
                source = f.read()
        except FileNotFoundError:
            print(f"Error: File '{source_file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    # Compile
    compiler = Compiler(source, verbose=verbose)
    success, output = compiler.compile()
    
    if not verbose:
        # In non-verbose mode, just show output
        for line in output:
            print(line)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

