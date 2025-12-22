import sys
import json
import os
from antlr4 import *
from PseudocodeLexer import PseudocodeLexer
from PseudocodeParser import PseudocodeParser
from PseudocodeVisitor import PseudocodeVisitor

# This class defines HOW we extract data from the code
class CodeStructureVisitor(PseudocodeVisitor):
    def __init__(self):
        self.functions = []

    # Visit a function declaration rule
    def visitFunctionDecl(self, ctx):
        # Extract function name
        func_name = ctx.ID().getText()
        
        # Extract parameters if they exist
        params = []
        if ctx.paramList():
            params = [p.getText() for p in ctx.paramList().ID()]
            
        # Get the full source text of this function for the LLM to read later
        # full_text = self.token_stream.getText(ctx.start, ctx.stop)
        input_stream = ctx.start.getInputStream()
        start_char = ctx.start.start
        stop_char = ctx.stop.stop
        
        full_text = input_stream.getText(start_char, stop_char)

        # Create our Metadata JSON object
        func_data = {
            "type": "function",
            "name": func_name,
            "parameters": params,
            "code_content": full_text
        }
        
        self.functions.append(func_data)
        return self.visitChildren(ctx)

def parse_file(file_path):
    input_stream = FileStream(file_path)
    lexer = PseudocodeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PseudocodeParser(stream)
    
    # Parse the 'program' rule
    tree = parser.program()
    
    # Use our visitor to walk the tree
    visitor = CodeStructureVisitor()
    visitor.visit(tree)
    
    return visitor.functions

# Main Execution
if __name__ == "__main__":
    all_code_chunks = []
    data_folder = "./data"
    
    # Loop through all .pseudo files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".avp"):
            print(f"Processing {filename}...")
            full_path = os.path.join(data_folder, filename)
            chunks = parse_file(full_path)
            all_code_chunks.extend(chunks)
            
    # Save the result to a JSON file (This is your "Database")
    with open("code_knowledge_base.json", "w") as f:
        json.dump(all_code_chunks, f, indent=4)
        
    print(f"Successfully indexed {len(all_code_chunks)} code blocks into code_knowledge_base.json")