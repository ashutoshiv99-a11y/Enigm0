import chromadb

def search_threat_intelligence(query):
    print(f"[*] Searching Global Threat Intelligence for: '{query}'...")
    try:
        # Connect to the local vector database you just built
        chroma_client = chromadb.PersistentClient(path="./brain/chroma_db")
        collection = chroma_client.get_collection(name="cyber_intelligence")
        
        # Search for the 2 most relevant pieces of data
        results = collection.query(query_texts=[query], n_results=2)
        
        if results and results['documents'] and len(results['documents'][0]) > 0:
            # Combine the top results into a single text block
            context = "\n---\n".join(results['documents'][0])
            return f"Here is the raw threat intelligence data from the MITRE framework:\n\n{context}"
        else:
            return "I have no data on that specific threat in my local memory."
    except Exception as e:
        print(f"[!] Error accessing ChromaDB: {e}")
        return "My cyber intelligence database is currently offline."

# Quick test block
if __name__ == "__main__":
    print(search_threat_intelligence("What is Pass the Hash?"))