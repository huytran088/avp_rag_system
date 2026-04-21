import json
import os
import sys
import warnings
from typing import Dict, List, Optional

import faiss
import numpy as np

# Suppress tokenizer warnings (safe — only affects Python warnings, not errors)
warnings.filterwarnings('ignore', category=UserWarning)
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Import FlagEmbedding with clear error handling instead of stderr suppression
try:
    from FlagEmbedding import FlagModel, FlagReranker
except ImportError as e:
    print(f"Error importing FlagEmbedding: {e}")
    print()
    print("This is likely a version mismatch between FlagEmbedding and transformers.")
    print("To fix, try one of the following:")
    print("  Option A: uv pip install --upgrade FlagEmbedding")
    print("  Option B: uv pip install transformers==4.44.2")
    sys.exit(1)


def _load_knowledge_base(path: str) -> List[Dict]:
    """Load the knowledge base JSON, supporting both legacy and tracked formats."""
    print(f"Loading knowledge base from {path}...")
    with open(path, "r") as f:
        data = json.load(f)

    if isinstance(data, list):
        # Old format - flat array
        print(f"Loaded {len(data)} code snippets (legacy format).")
        return data

    if isinstance(data, dict) and "chunks" in data:
        # New format - with metadata wrapper
        chunks = data["chunks"]
        metadata = data.get("metadata", {})
        print(f"Loaded {len(chunks)} code snippets (tracked format).")
        print(f"  Tracking method: {metadata.get('tracking_method', 'unknown')}")
        print(f"  Last ingestion: {metadata.get('last_ingestion', 'unknown')}")
        return chunks

    raise ValueError(f"Unknown knowledge base format in {path}")


def _normalize(vectors: np.ndarray) -> np.ndarray:
    """L2 normalize vectors for cosine similarity."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / (norms + 1e-10)  # Avoid div by 0


class CodeRetriever:
    """
    Two-stage retrieval system for code snippets.

    Stage 1: Fast vector search using UnXcoder emmbeddings + FAISS
    Stage 2: Accurate reranking using a cross encoder model
    """

    def __init__(
        self,
        knowledge_base_path: str = "code_knowledge_base.json",
        embedding_model: str = "BAAI/bge-base-en-v1.5",
        reranker_model: str = "BAAI/bge-reranker-base",
        use_reranker: bool = True,
        device: str = "cpu",  # change to "cuda" when GPU is available
    ):
        self.device = device
        self.use_reranker = use_reranker
        self.knowledge_base = _load_knowledge_base(knowledge_base_path)

        # Init the Embedding Model
        use_fp16 = (device == "cuda")
        print(f"Loading embedding model: {embedding_model}...")
        self.embedding_model = FlagModel(
            embedding_model,
            query_instruction_for_retrieval="Represent this sentence for searching relevant code:",
            use_fp16=use_fp16,
        )

        # Initialize the Reranker (Cross-Encoder)
        if use_reranker:
            print(f"Loading reranker model: {reranker_model}...")
            self.reranker = FlagReranker(reranker_model, use_fp16=use_fp16)
        else:
            self.reranker = None

        self._build_index()

    def _build_index(self):
        """Create FAISS index with normalized embeddings for cosine similarity."""
        print("Building vector index...")

        # Create a searchable text representation per function
        self.code_texts = [
            f"Function: {item['name']}({', '.join(item.get('parameters', []))})\n{item['code_content']}"
            for item in self.knowledge_base
        ]

        embeddings = self.embedding_model.encode(self.code_texts)
        self.embeddings = _normalize(embeddings).astype('float32')

        # Build FAISS index with Inner Product
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings)

        print(f"Index built successfully. Dimension: {dimension}, Vectors: {len(self.code_texts)}")

    def retrieve(
        self,
        query: str,
        k: int = 5,
        rerank_top_k: Optional[int] = None,
    ) -> List[Dict]:
        """
        Retrieve relevant code snippets for a query

        Args:
            query: Natural language query (e.g., "how to do a loop?")
            k: Number of final results to return
            rerank_top_k: Number of candidates to fetch before reranking.
                         If None, defaults to k * 3 (or k if reranker is disabled)

        Returns:
            List of dicts with keys: score, function_name, parameters, code
        """
        # Determine how many candidates to fetch for reranking
        if rerank_top_k is None:
            rerank_top_k = k * 3 if self.use_reranker else k
        # Limit the number of requests, no more than what we have
        rerank_top_k = min(rerank_top_k, len(self.knowledge_base))

        # Fast vector search
        query_vector = _normalize(self.embedding_model.encode_queries([query]))
        scores, indices = self.index.search(query_vector, rerank_top_k)

        # Gather candidates (scores are cosine similarities in [-1, 1])
        candidates = []
        for i in range(rerank_top_k):
            idx = indices[0][i]
            if idx < 0:  # Return -1 for missing results
                continue
            item = self.knowledge_base[idx]
            candidates.append({
                "index": idx,
                "initial_score": float(scores[0][i]),
                "function_name": item['name'],
                "parameters": item.get('parameters', []),
                "code": item['code_content'],
            })

        # Reranking
        if self.use_reranker and self.reranker and candidates:
            # Cross-encoder scoring on (query, code) pairs
            pairs = [[query, c['code']] for c in candidates]
            rerank_scores = self.reranker.compute_score(pairs)
            for c, rs in zip(candidates, rerank_scores):
                c['rerank_score'] = float(rs)
                c['score'] = float(rs)
            candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        else:
            for c in candidates:
                c['score'] = c['initial_score']

        # Return top-k results
        return [
            {
                "score": c['score'],
                "function_name": c['function_name'],
                "parameters": c['parameters'],
                "code": c['code'],
            }
            for c in candidates[:k]
        ]

    def retrieve_simple(self, query: str, k: int = 1) -> List[Dict]:
        """Backward compatible version of the retrieval function."""
        return self.retrieve(query, k=k)


# Global Retriever
_retriever: Optional[CodeRetriever] = None


def get_retriever() -> CodeRetriever:
    global _retriever
    if _retriever is None:
        _retriever = CodeRetriever()
    return _retriever


def retrieve_code(query: str, k: int = 1) -> List[Dict]:
    return get_retriever().retrieve(query, k=k)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   RAG Retrieval Demo")
    print("=" * 60)

    # Initialize retriever
    retriever = CodeRetriever(
        use_reranker=True,  # Set to False for faster but less accurate results
        device="cpu",       # Change to "cuda" when GPU is available
    )

    print("\nType 'exit' to quit.")
    print("Try queries like: 'how to do a loop?', 'find maximum value', 'search algorithm'")

    while True:
        user_query = input("\nYour question: ").strip()
        if user_query.lower() == 'exit':
            break
        if not user_query:
            continue

        matches = retriever.retrieve(user_query, k=3)

        print(f"\nFound {len(matches)} relevant code snippets:")
        print("-" * 50)

        for i, match in enumerate(matches, 1):
            print(f"\n[{i}] {match['function_name']}({', '.join(match['parameters'])})")
            print(f"    Score: {match['score']:.4f}")
            print(f"    Code preview: {match['code'][:100]}...")

        print("-" * 50)
