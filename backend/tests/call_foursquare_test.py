import requests
import asyncio
import pandas as pd
from app.config import Config

# Example LLM response (the input query from the user)
llm_response = {
    'action': 'restaurant_search',
    'parameters': {
        'query': 'Italian',
        'near': 'New York',
        'price': 'any',
        'open_now': True
    }
}

# API URL and Key
API_URL = "https://api.foursquare.com/v3/places/search"
API_KEY = Config.FOURSQUARE_KEY  # Replace with your API key

# Headers with API Key
HEADERS = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Extract parameters from the LLM response
params = {
    "query": llm_response['parameters'].get('query', 'restaurant'),
    "near": llm_response['parameters'].get('near'),
    "open_now": llm_response['parameters'].get('open_now', False),
}

# Map price levels if any (this is optional)
price_map = {
    'cheap': '1',
    'moderate': '2',
    'expensive': '3',
    'very expensive': '4'
}

price = llm_response['parameters'].get('price')
if price and price.lower() in price_map:
    params['price'] = price_map[price.lower()]

# Make the request to Foursquare API
response = requests.get(API_URL, headers=HEADERS, params=params)

restaurant_data = []
if response.status_code == 200:
    results = response.json().get("results", [])
    
    for item in results:
        # Extracting the desired fields from the response
        restaurant = {
            "Name": item.get("name"),
            "Address": item["location"].get("formatted_address"),
            "Cuisine": list(item["features"]["food_and_drink"]["meals"].keys()) if item.get("features") else [],
            "Rating": item.get("rating"),
            "Price Level": item.get("price")
        }
        
        # Check if 'hours' exists before trying to access it
        hours = item.get("hours", {})
        if hours:
            restaurant["Operating Hours"] = hours.get("regular", [])
        else:
            restaurant["Operating Hours"] = "Not Available"

        restaurant_data.append(restaurant)
else:
    print(f"Error fetching data: {response.status_code}, {response.text}")


for r in restaurant_data:
    print(r)
