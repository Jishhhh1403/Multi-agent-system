import chromadb
from typing import List, Optional
from pathlib import Path
from config.settings import settings

class DocumentMemory:
    """Manages code embeddings in ChromaDB for RAG retrieval."""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(settings.data_dir / "chroma_db")
        )
        self.collection = self.client.get_or_create_collection(
            name="codebase",
            metadata={"hnsw:space": "cosine"}
        )
    
    def ingest_file(self, file_path: Path, content: str) -> None:
        """Ingest a single file into the vector store."""
        chunks = self._chunk_text(content, file_path)
        
        if not chunks:
            return
        
        ids = [f"{file_path}::chunk::{i}" for i in range(len(chunks))]
        metadatas = [{"source": str(file_path), "chunk_index": i} for i in range(len(chunks))]
        
        self.collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )
    
    def ingest_directory(self, dir_path: Path, extensions: List[str] = None) -> int:
        """Ingest all files from a directory."""
        if extensions is None:
            extensions = [".py", ".md", ".txt", ".json"]
        
        count = 0
        for file_path in dir_path.rglob("*"):
            if file_path.suffix in extensions and file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    self.ingest_file(file_path, content)
                    count += 1
                except Exception as e:
                    print(f"Warning: Could not ingest {file_path}: {e}")
        
        return count
    
    def retrieve(self, query: str, k: int = None) -> List[dict]:
        """Retrieve relevant code chunks for a query."""
        if k is None:
            k = settings.retrieval_k
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "score": results["distances"][0][i] if results.get("distances") else None
            })
        
        return output
    
    def _chunk_text(self, text: str, file_path: Path, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into overlapping chunks."""
        if chunk_size is None:
            chunk_size = settings.chunk_size
        if overlap is None:
            overlap = settings.chunk_overlap
        
        # For code, try to split on meaningful boundaries
        if file_path.suffix == ".py":
            return self._chunk_python_code(text, chunk_size, overlap)
        
        # Generic text chunking
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        
        return chunks
    
    def _chunk_python_code(self, code: str, chunk_size: int, overlap: int) -> List[str]:
        """Split Python code on function/class boundaries."""
        lines = code.split("\n")
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            current_chunk.append(line)
            current_size += len(line) + 1
            
            # Split on function/class definitions or when chunk is full
            if (line.startswith("def ") or line.startswith("class ")) and current_size > 100:
                chunks.append("\n".join(current_chunk[:-1]))
                current_chunk = [current_chunk[-1]]
                current_size = len(line)
            elif current_size >= chunk_size:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append("\n".join(current_chunk))
        
        return chunks
    
    def clear(self) -> None:
        """Clear all data from the collection."""
        self.client.delete_collection("codebase")
        self.collection = self.client.get_or_create_collection(
            name="codebase",
            metadata={"hnsw:space": "cosine"}
        )