import os
import chromadb

def chunk_text(text, max_chars=1000):
    """Chops long text into smaller chunks so the AI can read them easily."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        if len(current_chunk) + len(p) < max_chars:
            current_chunk += p + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def build_owasp_memory():
    print("=== J.A.R.V.I.S. OWASP Intelligence Ingestion ===")
    
    # 1. Connect to the existing Vector Database
    db_path = "./brain/chroma_db"
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="cyber_intelligence")
    
    # 2. The folders you just cloned
    target_folders = ["./www-project-top-ten", "./wstg"]
    
    documents = []
    metadatas = []
    ids = []
    doc_id_counter = 0

    print("[*] Crawling OWASP repositories for Markdown files...")
    
    # 3. Walk through all folders and subfolders
    for folder in target_folders:
        if not os.path.exists(folder):
            print(f"[!] Warning: Could not find folder {folder}")
            continue
            
        for root, _, files in os.walk(folder):
            for file in files:
                # We only want to read Markdown files
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        # Ignore useless empty files
                        if len(content) < 50:
                            continue
                            
                        # Chop the file into smaller chunks
                        chunks = chunk_text(content)
                        
                        for i, chunk in enumerate(chunks):
                            documents.append(chunk)
                            # Save where this info came from so we know it's OWASP data
                            metadatas.append({"source": file, "framework": "OWASP"})
                            ids.append(f"owasp_{doc_id_counter}_{i}")
                            
                        doc_id_counter += 1
                    except Exception as e:
                        pass # Skip files that can't be read

    print(f"[*] Found and processed {len(documents)} blocks of OWASP web security data.")
    print("[*] Injecting into Vector Database... This might take a minute.")
    
    # 4. Add the data to ChromaDB in batches
    batch_size = 150
    total_batches = (len(documents) // batch_size) + 1
    
    for i in range(0, len(documents), batch_size):
        batch_num = (i // batch_size) + 1
        print(f"    -> Processing batch {batch_num}/{total_batches}...")
        
        collection.add(
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
        
    print("[***] Ingestion Complete! J.A.R.V.I.S. now has the OWASP framework memorized.")

if __name__ == "__main__":
    build_owasp_memory()