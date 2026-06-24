import json
import chromadb
import os

def build_mitre_memory():
    print("=== J.A.R.V.I.S. Threat Intelligence Ingestion ===")
    
    # 1. Initialize the permanent local Vector Database
    # This will create a folder called 'chroma_db' inside your 'brain' folder
    db_path = "./brain/chroma_db"
    os.makedirs(db_path, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    # Create or load the cyber security collection
    collection = chroma_client.get_or_create_collection(name="cyber_intelligence")
    
    # 2. Locate the MITRE ATT&CK data you just cloned
    stix_file = "./attack-stix-data/enterprise-attack/enterprise-attack.json"
    
    if not os.path.exists(stix_file):
        print(f"[!] Cannot find {stix_file}. Did you clone the repo in the right folder?")
        return

    print("[*] Loading MITRE Enterprise ATT&CK framework...")
    with open(stix_file, 'r', encoding='utf-8') as f:
        mitre_data = json.load(f)

    documents = []
    metadatas = []
    ids = []

    print("[*] Parsing hacking techniques, malware, and threat groups...")
    # 3. Extract the valuable data from the complex STIX JSON format
    for obj in mitre_data.get("objects", []):
        # We only want to memorize Attack Patterns (Techniques), Malware, and Intrusion Sets (Hackers)
        if obj.get("type") in ["attack-pattern", "malware", "intrusion-set"]:
            name = obj.get("name", "Unknown")
            description = obj.get("description", "")
            obj_id = obj.get("id", str(len(ids))) # Unique ID for the database
            
            # Skip empty entries
            if description:
                # Format the text so J.A.R.V.I.S. can easily read it later
                formatted_text = f"Entity: {name}\nType: {obj.get('type')}\nDescription: {description}"
                
                documents.append(formatted_text)
                metadatas.append({"name": name, "type": obj.get('type')})
                ids.append(obj_id)

    print(f"[*] Found {len(documents)} threat intelligence records. Injecting into Vector Database...")
    
    # 4. Add the data to ChromaDB in batches (so we don't crash the computer)
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
        
    print("[***] Ingestion Complete! J.A.R.V.I.S. now has the MITRE ATT&CK framework memorized.")
    print(f"[***] Database saved to: {db_path}")

if __name__ == "__main__":
    build_mitre_memory()