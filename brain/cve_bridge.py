import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the URI securely from the environment
MONGO_URI = os.getenv("MONGO_URI")

def search_nvd_database(query):
    """Searches the cloud MongoDB database for vulnerabilities."""
    
    # Safety check: Ensure the URI was actually loaded
    if not MONGO_URI:
        print("[!] Error: MONGO_URI environment variable not found. Check your .env file.")
        return "Database configuration error."

    print(f"[*] Querying MongoDB Atlas Threat Intel for: '{query}'...")
    
    try:
        client = MongoClient(MONGO_URI)
        db = client["threat_intel"] # Replace with your exact database name
        collection = db["cves"]     # Replace with your exact collection name
        
        # 1. Check if the user is asking for a specific CVE ID (e.g., CVE-2021-44228)
        if "CVE-" in query.upper():
            # Extract the CVE ID from the string
            words = query.upper().split()
            cve_id = next((word for word in words if "CVE-" in word), None)
            
            if cve_id:
                # Direct lookup
                result = collection.find_one({"cve.id": cve_id})
                if result:
                    return _format_cve_data(result)
                return f"No records found for {cve_id} in the database."

        # 2. Otherwise, do a text/regex search for keywords (e.g., "Log4j", "Windows 10 exploit")
        results = collection.find({
            "$or": [
                {"cve.descriptions.value": {"$regex": query, "$options": "i"}},
                {"cve.id": {"$regex": query, "$options": "i"}}
            ]
        }).sort("cve.id", -1).limit(3) # Get top 3 newest results
        
        data_list = list(results)
        
        if not data_list:
            return f"I found no vulnerabilities related to '{query}' in the global database."
            
        formatted_results = "\n\n".join([_format_cve_data(doc) for doc in data_list])
        return f"Found the following recent vulnerabilities:\n\n{formatted_results}"

    except Exception as e:
        print(f"[!] MongoDB Connection Error: {e}")
        return "I am unable to connect to the Atlas cloud database."

def _format_cve_data(doc):
    """Parses the messy NVD JSON into a clean string for the Groq AI to read."""
    cve_id = doc.get("cve", {}).get("id", "Unknown ID")
    
    # Safely extract description
    descriptions = doc.get("cve", {}).get("descriptions", [])
    desc_text = descriptions[0].get("value", "No description available.") if descriptions else "No description available."
    
    # Safely extract CVSS Severity Score (Handles both v2, v3, and v31 schemas)
    metrics = doc.get("cve", {}).get("metrics", {})
    score = "Unknown"
    severity = "Unknown"
    
    if "cvssMetricV31" in metrics:
        score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
        severity = metrics["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
    elif "cvssMetricV3" in metrics:
        score = metrics["cvssMetricV3"][0]["cvssData"]["baseScore"]
        severity = metrics["cvssMetricV3"][0]["cvssData"]["baseSeverity"]
    elif "cvssMetricV2" in metrics:
        score = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
        severity = metrics["cvssMetricV2"][0]["baseSeverity"]

    return f"ID: {cve_id}\nSeverity: {severity} ({score}/10)\nDescription: {desc_text}"

if __name__ == "__main__":
    # Test your bridge!
    print(search_nvd_database("Log4j"))