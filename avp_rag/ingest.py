"""Parse .avp files with ANTLR and build the code knowledge base."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

from antlr4 import CommonTokenStream, FileStream

from . import config
from .knowledge_base import PathLike, load_kb, save_kb
from .parser import PseudocodeLexer, PseudocodeParser, PseudocodeVisitor
from .tracking import (
    detect_changed_files,
    remove_deleted_from_metadata,
    resolve_source_key,
    update_metadata,
)


class CodeStructureVisitor(PseudocodeVisitor):
    """Collects every function declaration with its params and full source text."""

    def __init__(self, source_file: str | None = None):
        self.functions: List[Dict] = []
        self.source_file = source_file

    def visitFunctionDecl(self, ctx):
        func_name = ctx.ID().getText()  # type: ignore[union-attr]

        params = [p.ID().getText() for p in ctx.paramList().annotatedParam()] if ctx.paramList() else []  # type: ignore[union-attr,misc]

        # Full source text of this function, for the LLM to read later
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


def parse_file(file_path: PathLike, source_file: str | None = None) -> List[Dict]:
    lexer = PseudocodeLexer(FileStream(str(file_path)))
    parser = PseudocodeParser(CommonTokenStream(lexer))
    tree = parser.program()

    visitor = CodeStructureVisitor(source_file=source_file)
    visitor.visit(tree)
    return visitor.functions


@dataclass
class IngestResult:
    chunks: List[Dict]
    metadata: Dict
    previous_ingestion: str | None
    changed: List[str]
    unchanged: List[str]
    deleted: List[str]
    preserved_count: int
    extracted: Dict[str, List[str]] = field(default_factory=dict)
    failed: List[Tuple[str, str]] = field(default_factory=list)


def run_ingest(
    data_dir: PathLike = config.DATA_DIR,
    kb_path: PathLike = config.KB_PATH,
) -> IngestResult:
    """Incrementally (re)ingest data_dir into kb_path and save it."""
    existing_chunks, metadata = load_kb(kb_path)
    previous_ingestion = metadata.get("last_ingestion")

    changed, unchanged, deleted = detect_changed_files(data_dir, metadata)
    if deleted:
        metadata = remove_deleted_from_metadata(metadata, deleted)

    # Keep chunks from unchanged files; changed/deleted ones get dropped (and changed re-parsed)
    excluded = set(changed) | set(deleted)
    chunks = [c for c in existing_chunks if c.get("source_file") not in excluded]
    preserved_count = len(chunks)

    extracted: Dict[str, List[str]] = {}
    failed: List[Tuple[str, str]] = []
    for key in changed:
        try:
            file_chunks = parse_file(resolve_source_key(key), source_file=key)
        except Exception as e:
            failed.append((key, str(e)))
            continue
        chunks.extend(file_chunks)
        names = [c["name"] for c in file_chunks]
        metadata = update_metadata(metadata, key, names)
        extracted[key] = names

    save_kb(chunks, metadata, kb_path)

    return IngestResult(
        chunks=chunks,
        metadata=metadata,
        previous_ingestion=previous_ingestion,
        changed=changed,
        unchanged=unchanged,
        deleted=deleted,
        preserved_count=preserved_count,
        extracted=extracted,
        failed=failed,
    )


def _print_file_list(label: str, files: List[str]) -> None:
    print(f"\n{label}: {len(files)}")
    for f in files:
        print(f"  - {Path(f).name}")


def main() -> None:
    print("=" * 60)
    print("AVP Code Ingestion with Change Tracking")
    print("=" * 60)
    print(f"\nScanning {config.DATA_DIR} for {config.SOURCE_EXTENSION} files...")

    result = run_ingest()

    if result.previous_ingestion:
        print(f"Last ingestion: {result.previous_ingestion}")
    else:
        print("No previous ingestion found. Processed all files.")

    _print_file_list("Changed files", result.changed)
    _print_file_list("Unchanged files", result.unchanged)
    _print_file_list("Deleted files", result.deleted)
    print(f"\nPreserved {result.preserved_count} chunks from unchanged files.")

    for key, names in result.extracted.items():
        print(f"  {Path(key).name}: {len(names)} function(s): {', '.join(names)}")
    if not result.changed:
        print("\nNo files changed. Knowledge base is up to date.")

    if result.failed:
        print(f"\nWARNING: {len(result.failed)} file(s) failed to parse:")
        for key, error in result.failed:
            print(f"  - {Path(key).name}: {error}")

    print("=" * 60)
    print(f"Successfully indexed {len(result.chunks)} code blocks into {config.KB_PATH.name}")
    print(f"Tracking method: {result.metadata.get('tracking_method', 'hash')}")
    print(f"Total source files: {len(result.metadata.get('source_files', {}))}")
    print("=" * 60)


if __name__ == "__main__":
    main()
