import json
import numpy as np
import faiss
# from sentence_transformers import SentenceTransformer, CrossEncoder
from FlagEmbedding import FlagModel, FlagReranker
from typing import List, Dict, Optional

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
        device: str = "cpu" # change to "cuda" when GPU is available
    ):
        self.device = device
        self.use_reranker = use_reranker
        
        # Load the knowledge base
        print(f"Loading knowledge base from {knowledge_base_path}...")
        with open(knowledge_base_path, "r") as f:
            self.knowledge_base = json.load(f)
        print(f"Loaded {len(self.knowledge_base)} code snippets.")
        
        # Init the Embedding Model
        use_fp16 = (device == "cuda")
        print(f"Loading embedding model: {embedding_model}...")
        self.embedding_model = FlagModel(
            embedding_model,
            query_instruction_for_retrieval = "Represent this sentence for searching relevant code:",
            use_fp16=use_fp16
        )
        
        # Initialize the Reranker (Cross-Encoder)
        if use_reranker:
            print(f"Loading reranker model: {reranker_model}...")
            self.reranker = FlagReranker(reranker_model, use_fp16=use_fp16)
        else:
            self.reranker = None
            
        # Build the index
        self._build_index()
        
    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        """
        L2 normalize vectors for cosing similarity.
        """
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-10) # Avoid div by 0
        
    def _build_index(self):
        """
        Create FAISS index with normailized embeddings for cosine similarity
        """
        
        print("Building vector index...")
        
        # Extract code for embeddings
        self.code_texts = []
        for item in self.knowledge_base:
            # Create a searchable text representation
            params_str = ", ".join(item.get("parameters", []))
            text = f"Function: {item['name']}({params_str})\n{item['code_content']}"
            self.code_texts.append(text)
            
        # Generate embeddings
        # self.embeddings = self.embedding_model.encode(
        #     self.code_texts,
        #     normalized_embeddings=True,
        #     show_progress_bar=True
        # )
        self.embeddings = self.embedding_model.encode(self.code_texts)
        self.embeddings = self._normalize(self.embeddings).astype('float32')
        
        # Build FAISS index with Inner Product
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings)
        
        print(f"Index built successfully. Dimension: {dimension}, Vectors: {len(self.code_texts)}")
        
    def retrieve(
        self,
        query: str,
        k: int = 5,
        rerank_top_k: Optional[int] = None
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
        query_vector = self.embedding_model.encode_queries([query])
        query_vector = self._normalize(query_vector)
        # Search (scores are cosine similarities in range [-1, 1])
        scores, indices = self.index.search(query_vector, rerank_top_k)
        
        # Gather candidates
        candidates = []
        for i in range(rerank_top_k):
            idx = indices[0][i]
            if idx < 0: # Return -1 for missing results
                continue
            candidates.append({
                "index" : idx,
                "initial_score" : float(scores[0][i]),
                "function_name": self.knowledge_base[idx]['name'],
                "parameters" : self.knowledge_base[idx].get('parameters', []),
                "code": self.knowledge_base[idx]['code_content']
            })
            
        # Reranking
        if self.use_reranker and self.reranker and len(candidates) > 0:
            # Prepare query-document pairs for the cross-encoder
            pairs = [[query, c['code']] for c in candidates]
            
            # Get reranker scores
            rerank_scores = self.reranker.compute_score(pairs)
            
            for i, candidate in enumerate(candidates):
                candidate['rerank_score'] = float(rerank_scores[i])
            
            # Sort by rerank score in descending order
            candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
            
            for c in candidates:
                c['score'] = c['rerank_score']
        else:
            for c in candidates:
                c['score'] = c['initial_score']
                
        # Return top-k results
        results = []
        for c in candidates[:k]:
            results.append({
                "score": c['score'],
                "function_name": c['function_name'],
                "parameters": c['parameters'],
                "code": c['code'] 
            })
        return results
    
    def retrieve_simple(self, query: str, k: int = 1) -> List[Dict]:
        """
        Backward compatible version of the retrieval function
        """
        return self.retrieve(query, k=k)
        
# Global Retriever
_retriever: Optional[CodeRetriever] = None

def get_retriever() -> CodeRetriever:
    global _retriever
    if _retriever is None:
        _retriever = CodeRetriever()
    return _retriever

def retrieve_code(query: str, k: int = 1) -> List[Dict]:
    retriever = get_retriever()
    return retriever.retrieve(query, k=k)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   RAG Retrieval Demo")
    print("="*60)
    
    # Initialize retriever
    retriever = CodeRetriever(
        use_reranker=True,  # Set to False for faster but less accurate results
        device="cpu"        # Change to "cuda" when GPU is available
    )
    
    print("\nType 'exit' to quit.")
    print("Try queries like: 'how to do a loop?', 'find maximum value', 'search algorithm'")
    
    while True:
        user_query = input("\nYour question: ").strip()
        if user_query.lower() == 'exit':
            break
        if not user_query:
            continue
        
        # Retrieve with reranking
        matches = retriever.retrieve(user_query, k=3)
        
        print(f"\nFound {len(matches)} relevant code snippets:")
        print("-" * 50)
        
        for i, match in enumerate(matches, 1):
            print(f"\n[{i}] {match['function_name']}({', '.join(match['parameters'])})")
            print(f"    Score: {match['score']:.4f}")
            print(f"    Code preview: {match['code'][:100]}...")
        
        print("-" * 50)