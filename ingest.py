import os

from antlr4 import CommonTokenStream, FileStream

from PseudocodeLexer import PseudocodeLexer
from PseudocodeParser import PseudocodeParser
from PseudocodeVisitor import PseudocodeVisitor
from tracking import (
    detect_changed_files,
    load_existing_chunks,
    load_metadata,
    remove_deleted_from_metadata,
    save_with_metadata,
    update_metadata,
)


# This class defines HOW we extract data from the code
class CodeStructureVisitor(PseudocodeVisitor):
    def __init__(self, source_file=None):
        self.functions = []
        self.source_file = source_file

    # Visit a function declaration rule
    def visitFunctionDecl(self, ctx):
        func_name = ctx.ID().getText()  # type: ignore[union-attr]

        # Extract parameters if they exist
        params = [p.ID().getText() for p in ctx.paramList().annotatedParam()] if ctx.paramList() else []  # type: ignore[union-attr,misc]

        # Get the full source text of this function for the LLM to read later
        input_stream = ctx.start.getInputStream()  # type: ignore[union-attr]
        full_text = input_stream.getText(ctx.start.start, ctx.stop.stop)  # type: ignore[union-attr]

        func_data = {
            "type": "function",
            "name": func_name,
            "parameters": params,
            "code_content": full_text,
        }
        if self.source_file:
            func_data["source_file"] = self.source_file

        self.functions.append(func_data)
        return self.visitChildren(ctx)


def parse_file(file_path, source_file=None):
    lexer = PseudocodeLexer(FileStream(file_path))
    parser = PseudocodeParser(CommonTokenStream(lexer))

    # Parse the 'program' rule
    tree = parser.program()

    visitor = CodeStructureVisitor(source_file=source_file)
    visitor.visit(tree)

    return visitor.functions


def _print_file_list(label: str, files: list) -> None:
    print(f"\n{label}: {len(files)}")
    for f in files:
        print(f"  - {os.path.basename(f)}")


# Main Execution
if __name__ == "__main__":
    data_folder = "./data"
    kb_path = "code_knowledge_base.json"

    print("=" * 60)
    print("AVP Code Ingestion with Change Tracking")
    print("=" * 60)

    # Load existing metadata and chunks
    print("\nLoading existing knowledge base...")
    metadata = load_metadata(kb_path)
    existing_chunks = load_existing_chunks(kb_path)

    if metadata.get("last_ingestion"):
        print(f"Last ingestion: {metadata['last_ingestion']}")
        print(f"Tracked files: {len(metadata.get('source_files', {}))}")
    else:
        print("No previous ingestion found. Will process all files.")

    # Detect changed files
    print(f"\nScanning {data_folder} for .avp files...")
    changed_files, unchanged_files, deleted_files = detect_changed_files(data_folder, metadata)

    _print_file_list("Changed files", changed_files)
    _print_file_list("Unchanged files", unchanged_files)
    _print_file_list("Deleted files", deleted_files)

    # Remove deleted files from metadata
    if deleted_files:
        print(f"\nRemoving {len(deleted_files)} deleted file(s) from metadata...")
        metadata = remove_deleted_from_metadata(metadata, deleted_files)

    # Start with existing chunks, but remove chunks from changed/deleted files
    excluded_files = set(changed_files) | set(deleted_files)
    all_code_chunks = []
    if existing_chunks:
        print(f"\nPreserving {len(existing_chunks)} existing chunks...")
        all_code_chunks = [c for c in existing_chunks if c.get("source_file") not in excluded_files]
        print(f"Preserved {len(all_code_chunks)} chunks from unchanged files.")

    # Process changed files
    failed_files = []
    if changed_files:
        print(f"\nProcessing {len(changed_files)} changed file(s)...")
        for full_path in changed_files:
            filename = os.path.basename(full_path)
            print(f"  Parsing {filename}...")

            try:
                chunks = parse_file(full_path, source_file=full_path)
                all_code_chunks.extend(chunks)

                function_names = [chunk["name"] for chunk in chunks]
                metadata = update_metadata(metadata, full_path, function_names)

                print(f"    Extracted {len(chunks)} function(s): {', '.join(function_names)}")
            except Exception as e:
                failed_files.append((full_path, str(e)))
                print(f"    ERROR: Failed to parse {filename}: {e}")
    else:
        print("\nNo files changed. Knowledge base is up to date.")

    # Report failed files
    if failed_files:
        print(f"\nWARNING: {len(failed_files)} file(s) failed to parse:")
        for path, error in failed_files:
            print(f"  - {os.path.basename(path)}: {error}")

    # Save with metadata wrapper
    print("\nSaving knowledge base...")
    save_with_metadata(all_code_chunks, metadata, kb_path)

    print("=" * 60)
    print(f"Successfully indexed {len(all_code_chunks)} code blocks")
    print(f"Tracking method: {metadata.get('tracking_method', 'hash')}")
    print(f"Total source files: {len(metadata.get('source_files', {}))}")
    print("=" * 60)
