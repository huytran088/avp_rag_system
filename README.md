# AVP Pseudocode RAG System

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)

A Retrieval-Augmented Generation (RAG) system for the AVP pseudocode language. Uses ANTLR4 to parse AVP source files, extracts function metadata into a searchable knowledge base, and provides semantic code retrieval with optional reranking for LLM-powered code generation.

## Features

- **ANTLR4 Grammar** - Full parser for the AVP pseudocode language
- **Function Extraction** - Automatically extracts and indexes function declarations with metadata
- **Two-Stage Retrieval** - Fast vector search using BGE embeddings + FAISS, with optional BGE reranker for improved accuracy
- **RAG Generation** - Builds context-aware prompts for LLM code generation

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────────────┐
│  .avp files │────▶│ ANTLR Parser │────▶│ JSON Knowledge Base│
└─────────────┘     └──────────────┘     └─────────┬──────────┘
                                                   │
                    ┌──────────────┐     ┌─────────▼──────────┐
                    │  LLM Prompt  │◀────│  Vector Retrieval  │
                    └──────────────┘     └────────────────────┘
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- ANTLR4 (only needed for grammar regeneration)

## Installation

```bash
git clone <repository-url>
cd antlr4_tut
uv sync
```

## Usage

### 1. Ingest AVP Files

Parse all `.avp` files in the `data/` folder and build the knowledge base:

```bash
uv run python ingest.py
```

This creates `code_knowledge_base.json` with extracted function metadata.

### 2. Retrieve Code

Run the interactive retrieval demo to search for relevant code snippets:

```bash
uv run python retrieve.py
```

### 3. Generate Code

Run the RAG generation demo to create new AVP code based on natural language queries:

```bash
uv run python generate.py
```

### Regenerate Parser (after grammar changes)

```bash
antlr4 -Dlanguage=Python3 -visitor Pseudocode.g4
```

## Project Structure

```
├── Pseudocode.g4          # ANTLR4 grammar definition
├── PseudocodeLexer.py     # Generated lexer
├── PseudocodeParser.py    # Generated parser
├── PseudocodeVisitor.py   # Generated visitor
├── ingest.py              # Parses AVP files, builds knowledge base
├── retrieve.py            # Two-stage semantic retrieval
├── generate.py            # RAG prompt generation
├── data/                  # Sample AVP source files
│   ├── algorithms.avp
│   ├── array_ops.avp
│   ├── logic.avp
│   └── math_utils.avp
└── PseudocodeSyntax.md    # AVP language reference
```

## AVP Language

AVP is a Python-like pseudocode language designed for algorithm visualization. Example:

```
fun factorial(n):
    if (n <= 1):
        return 1
    end if
    return n * factorial(n - 1)
end fun
```

See [PseudocodeSyntax.md](PseudocodeSyntax.md) for the full language reference.

## License

MIT
