# Enigm0/brain/memory.py
import chromadb
from chromadb.utils import embedding_functions

class AssistantMemory:
    def __init__(self):
        # 1. Initialize local storage (This creates a 'memory_data' folder in your project)
        self.client = chromadb.PersistentClient(path="./brain/memory_data")
        
        # 2. Use a lightweight local embedding model to convert text to vectors
        self.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # 3. Create or load the 'user_facts' collection
        self.collection = self.client.get_or_create_collection(
            name="user_facts", 
            embedding_function=self.sentence_transformer_ef
        )
        print("[*] Memory Core Initialized.")

    def store_memory(self, text_fact):
        """Saves a new fact into the database."""
        # We need a unique ID for each memory. We'll just use a timestamp.
        import time
        doc_id = f"mem_{int(time.time())}"
        
        self.collection.add(
            documents=[text_fact],
            ids=[doc_id]
        )
        print(f"[*] Memory stored: {text_fact}")

    def recall_memory(self, query, n_results=2):
        """Searches the database for memories related to the query."""
        # If the database is empty, return nothing
        if self.collection.count() == 0:
            return ""
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # The results come back as a list of lists. We extract the actual text strings.
        retrieved_facts = results['documents'][0]
        
        if retrieved_facts:
             # Combine the facts into one string
            memory_context = " ".join(retrieved_facts)
            print(f"[*] Memory recalled: {memory_context}")
            return memory_context
        return ""

# Quick test block: Only runs if you execute memory.py directly
if __name__ == "__main__":
    mem = AssistantMemory()
    mem.store_memory("My favorite programming language is Python.")
    mem.store_memory("I am currently building a local AI assistant named Enigma.")
    
    print("\n--- Testing Recall ---")
    mem.recall_memory("What language do I like?")