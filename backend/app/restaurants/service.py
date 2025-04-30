from openai import OpenAI
import httpx  # <-- replaced 'requests'
import json

from .schemas import RestaurantSearch, Restaurant
from app.config import Config

client = OpenAI(api_key=Config.OPEN_AI_KEY)

# Use Hugging Face pipeline for text generation (you can use other models depending on your needs)
async def get_llm_json_command(user_input: str) -> RestaurantSearch:
    prompt = f"""
    Convert the following user message into a JSON command to search for restaurants.
    User Input: "{user_input}"

    Expected Schema:
    {{
        "action": "restaurant_search",
        "parameters": {{
            "query": "<type of food>",
            "near": "<location>",
            "price": "<price level>",  // optional
            "open_now": <true or false>  // optional
        }}
    }}

    Return only valid JSON.
    """

    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # change here!
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs JSON based on user input."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

        json_str = response.choices[0].message.content.strip()
        json_data = json.loads(json_str)  # ✅ SAFER than eval()
        return RestaurantSearch(**json_data)  # ✅ Use Pydantic validation
    except Exception as e:
        print(f"Error in LLM response: {e}")
        return None




async def call_foursquare_api(json_command: RestaurantSearch) -> list[Restaurant]:
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": f"Bearer {Config.FOURSQUARE_KEY}"
    }

    params = {
        "query": json_command.parameters.query,
        "near": json_command.parameters.near,
        "price": json_command.parameters.price or "",
        "open_now": json_command.parameters.open_now or False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            return [
                Restaurant(
                    name=restaurant["name"],
                    address=restaurant.get("location", {}).get("address", "N/A"),
                    rating=restaurant.get("rating", None),
                    price_level=restaurant.get("price", None),
                    hours=restaurant.get("hours", {}).get("status", None)
                )
                for restaurant in data.get("results", [])
            ]
    except Exception as e:
        print(f"Error in Foursquare API call: {e}")
        return []
