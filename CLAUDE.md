# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) system for generating code in the AVP pseudocode language. It uses ANTLR4 to parse AVP source files, extracts function metadata into a knowledge base, and provides semantic code retrieval with reranking.

## Commands

**Regenerate ANTLR parser files from grammar:**
```bash
antlr4 -Dlanguage=Python3 -visitor Pseudocode.g4
```

**Ingest AVP files into knowledge base:**
```bash
uv run python ingest.py
```
This parses all `.avp` files in `./data/` and outputs `code_knowledge_base.json`.

**Run retrieval demo:**
```bash
uv run python retrieve.py
```

**Run generation demo:**
```bash
uv run python generate.py
```

## Architecture

### RAG Pipeline
1. **Ingest** (`ingest.py`): Uses ANTLR4 to parse `.avp` files, extracts function declarations via `CodeStructureVisitor`, outputs JSON knowledge base
2. **Retrieve** (`retrieve.py`): Two-stage retrieval using BGE embeddings + FAISS for fast vector search, optional BGE reranker for accuracy
3. **Generate** (`generate.py`): Builds prompts with retrieved code context for LLM code generation

### ANTLR Components
- `Pseudocode.g4`: Grammar definition for the AVP language
- `PseudocodeLexer.py`, `PseudocodeParser.py`, `PseudocodeVisitor.py`: Generated parser files (regenerate after grammar changes)

### AVP Language Notes
- Python-like syntax with `fun`/`end fun`, `if`/`end if`, `for`/`end for`, `while`/`end while`
- Newlines are significant (statement separators)
- Strict 4-space indentation
- Keywords: `fun`, `for`, `in`, `if`, `else`, `while`, `return`, `break`, `end`, `and`, `or`, `True`, `False`
- Arrays: `[1, 2, 3]`, `[1 to 5]` (range), `(100)` (size)
- Comments: `// comment`
