import urllib.parse
import certifi
from pymongo import MongoClient

# ==========================================
# CONFIGURATION - PUT YOUR CREDENTIALS HERE
# ==========================================
MONGO_USERNAME = "Ashutosh_99"
MONGO_PASSWORD = "Ankita909090"
MONGO_CLUSTER = "cluster0.iiz0yoy.mongodb.net" # Example: cluster0.abcde.mongodb.net

escaped_user = urllib.parse.quote_plus(MONGO_USERNAME)
escaped_pass = urllib.parse.quote_plus(MONGO_PASSWORD)
MONGO_URI = f"mongodb+srv://{escaped_user}:{escaped_pass}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

def connect_db():
    print("Connecting to Threat Intel Database...")
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['threat_intel']
    return db['vulnerabilities']

def extract_cve_info(vuln):
    """Universal Extractor: Handles both NVD 2.0 and Legacy 1.1 formats"""
    cve_data = vuln.get('cve', vuln)
    
    # 1. Extract ID
    cve_id = cve_data.get('id')
    if not cve_id and 'CVE_data_meta' in cve_data:
        cve_id = cve_data['CVE_data_meta'].get('ID')
    if not cve_id:
        cve_id = vuln.get('id', 'UNKNOWN_ID')
        
    # 2. Extract Description
    desc_text = "No description available."
    if 'descriptions' in cve_data:
        for d in cve_data['descriptions']:
            if d.get('lang') == 'en': 
                desc_text = d.get('value')
                break
    elif 'description' in cve_data:
        for d in cve_data['description'].get('description_data', []):
            if d.get('lang') == 'en': 
                desc_text = d.get('value')
                break

    # 3. Extract Severity
    severity = "UNSCORED"
    metrics = cve_data.get('metrics', vuln.get('impact', {}))
    
    if 'cvssMetricV31' in metrics:
        severity = metrics['cvssMetricV31'][0].get('cvssData', {}).get('baseSeverity', 'UNKNOWN')
    elif 'cvssMetricV30' in metrics:
        severity = metrics['cvssMetricV30'][0].get('cvssData', {}).get('baseSeverity', 'UNKNOWN')
    elif 'cvssMetricV2' in metrics:
        severity = metrics['cvssMetricV2'][0].get('baseSeverity', 'UNKNOWN')
    elif 'baseMetricV3' in metrics:
        severity = metrics['baseMetricV3'].get('cvssV3', {}).get('baseSeverity', 'UNKNOWN')
    elif 'baseMetricV2' in metrics:
        severity = metrics['baseMetricV2'].get('severity', 'UNKNOWN')
        
    return {'id': cve_id, 'severity': severity, 'description': desc_text}

def print_vulnerability(info):
    print(f"\n==================================================")
    print(f"🚨 {info['id']} | Severity: {info['severity']}")
    print(f"==================================================")
    print(f"Description: {info['description']}")
    print(f"==================================================\n")

def search_by_cve(collection, cve_id):
    print(f"\nSearching for {cve_id}...")
    cve_id = cve_id.upper()
    
    # Search across all possible ID locations
    query = {
        "$or": [
            {"cve.id": cve_id},
            {"cve.CVE_data_meta.ID": cve_id},
            {"id": cve_id}
        ]
    }
    result = collection.find_one(query)
    
    if result:
        print_vulnerability(extract_cve_info(result))
    else:
        print(f"\n❌ Could not find {cve_id} in the database.")

def search_by_keyword(collection, keyword, limit=5):
    print(f"\nSearching for '{keyword}' (Showing top {limit})...")
    
    # Search across both modern and legacy description locations!
    query = {
        "$or": [
            {"cve.descriptions.value": {"$regex": keyword, "$options": "i"}},
            {"cve.description.description_data.value": {"$regex": keyword, "$options": "i"}}
        ]
    }
    
    # THE FIX: Tell MongoDB to sort the results by CVE ID (Newest to Oldest) 
    # BEFORE it limits the batch.
    results = collection.find(query).sort("cve.id", -1).limit(limit)
    
    count = 0
    for result in results:
        print_vulnerability(extract_cve_info(result))
        count += 1
        
    if count == 0:
        print(f"\n❌ No vulnerabilities found mentioning '{keyword}'.")

def main():
    collection = connect_db()
    print("✅ Connected successfully!\n")
    
    while True:
        print("\n--- ENIGM0 THREAT INTEL ENGINE ---")
        print("1. Lookup a specific CVE (e.g., CVE-2021-44228)")
        print("2. Search by Keyword (e.g., Log4j, Windows 11)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            cve_id = input("Enter CVE ID: ")
            search_by_cve(collection, cve_id)
        elif choice == '2':
            keyword = input("Enter keyword or software name: ")
            search_by_keyword(collection, keyword, limit=5)
        elif choice == '3':
            print("Shutting down engine. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()