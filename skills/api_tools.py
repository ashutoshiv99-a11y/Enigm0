import requests
import urllib.parse
from bs4 import BeautifulSoup # You will need to run: pip install beautifulsoup4

def get_crypto_price(coin):
    """Fetches live cryptocurrency prices from CoinGecko."""
    print(f"[*] Fetching live price for {coin}...")
    
    mapping = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana"
    }
    target_coin = mapping.get(coin.lower(), coin.lower())
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={target_coin}&vs_currencies=usd"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if target_coin in data:
            price = data[target_coin]['usd']
            formatted_price = "{:,.2f}".format(price)
            return f"The current live price of {target_coin} is {formatted_price} dollars."
        else:
            return f"I couldn't find a price for the coin named {coin}."
            
    except Exception as e:
        print(f"[!] API Error: {e}")
        return "I am unable to connect to the cryptocurrency market right now."

def get_weather(city):
    """Fetches live weather data from wttr.in."""
    print(f"[*] Fetching live weather for {city}...")
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        temp_c = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"The current weather in {city} is {desc} with a temperature of {temp_c} degrees Celsius."
    except Exception as e:
        print(f"[!] API Error: {e}")
        return f"I am unable to connect to the weather network for {city}."

def search_web(query):
    """Performs a web search using DuckDuckGo HTML to scrape the top result."""
    print(f"[*] Searching the web for: {query}...")
    
    # We use DuckDuckGo HTML version because it doesn't block scrapers as aggressively as Google
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the snippet from the first search result
        result_snippet = soup.find('a', class_='result__snippet')
        
        if result_snippet:
            snippet_text = result_snippet.text.strip()
            return f"According to the web: {snippet_text}"
        else:
            return "I couldn't find a direct answer on the web for that query."
            
    except Exception as e:
        print(f"[!] Web Search Error: {e}")
        return "I am currently unable to access the internet to search for that."

def route_api_request(target):
    """Routes the API request."""
    if ":" not in target:
        return "Invalid API request format."
        
    request_type, query = target.split(":", 1)
    
    if request_type == "crypto":
        return get_crypto_price(query)
    elif request_type == "weather":
        return get_weather(query)
    elif request_type == "search":
        return search_web(query)
    else:
        return f"I don't have an API tool installed for {request_type}."