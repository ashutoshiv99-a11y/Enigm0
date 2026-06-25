import os
import requests
import time
import certifi
import urllib.parse
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient, UpdateOne

# Load environment variables from the hidden .env file
load_dotenv()

# ==========================================
# CONFIGURATION - SECURED VIA .ENV
# ==========================================
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
NVD_API_KEY = os.getenv("NVD_API_KEY")

# Securely parse credentials
escaped_user = urllib.parse.quote_plus(MONGO_USERNAME)
escaped_pass = urllib.parse.quote_plus(MONGO_PASSWORD)
MONGO_URI = f"mongodb+srv://{escaped_user}:{escaped_pass}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

# NVD API Details
NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
HEADERS = {"apiKey": NVD_API_KEY}

def setup_database():
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['threat_intel']
    return db['vulnerabilities']

def fetch_recent_cves(collection):
    # Calculate dates: Get everything modified in the last 3 days (to provide a safe overlap)
    now = datetime.now(timezone.utc)
    three_days_ago = now - timedelta(days=3)
    
    # NIST requires a very specific time format (ISO 8601)
    end_date = now.strftime("%Y-%m-%dT%H:%M:%S.000")
    start_date = three_days_ago.strftime("%Y-%m-%dT%H:%M:%S.000")
    
    print(f"Fetching vulnerabilities modified between {start_date} and {end_date}...")

    results_per_page = 2000
    start_index = 0
    total_results = 1 # Placeholder
    
    while start_index < total_results:
        params = {
            "lastModStartDate": start_date,
            "lastModEndDate": end_date,
            "resultsPerPage": results_per_page,
            "startIndex": start_index
        }
        
        try:
            response = requests.get(NVD_BASE_URL, headers=HEADERS, params=params, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('totalResults', 0)
                vulnerabilities = data.get('vulnerabilities', [])
                
                if not vulnerabilities:
                    print("No new vulnerabilities found in this timeframe.")
                    break
                    
                # We use "UpdateOne" with upsert=True. 
                # This means: "If the CVE exists, update it with new info. If it doesn't exist, insert it."
                operations = []
                for item in vulnerabilities:
                    cve_data = item.get('cve', {})
                    cve_id = cve_data.get('id')
                    if cve_id:
                        operations.append(
                            UpdateOne({'cve.id': cve_id}, {'$set': item}, upsert=True)
                        )
                
                if operations:
                    result = collection.bulk_write(operations, ordered=False)
                    print(f"✅ Processed {len(operations)} records. (Inserted: {result.upserted_count}, Updated: {result.modified_count})")

                start_index += results_per_page
                time.sleep(6) # Polite sleep for API limits
                
            elif response.status_code in [403, 503]:
                print(f"Server busy ({response.status_code}). Retrying in 15 seconds...")
                time.sleep(15)
            else:
                print(f"Error {response.status_code}. Retrying...")
                time.sleep(10)
                
        except requests.exceptions.RequestException as e:
            print("Connection dropped. Retrying in 15 seconds...")
            time.sleep(15)

if __name__ == "__main__":
    db_collection = setup_database()
    fetch_recent_cves(db_collection)
    print("\n🎉 Daily Sync Complete! Your database is fully up to date.")