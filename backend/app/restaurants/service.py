from typing import List
from fastapi import HTTPException
import httpx
from app.llm.llm import HuggingFaceLLM  # Assuming HuggingFaceLLM is properly implemented elsewhere
from .schemas import RestaurantSearch, Restaurant
from app.config import Config

# A map for price levels (could be expanded)
price_map = {
    "cheap": 1,
    "medium": 2,
    "expensive": 3
}

class RestaurantService:
    def __init__(self, llm_instance: HuggingFaceLLM):
        """
        Initializes the service with the LLM instance.
        """
        self.llm_instance = llm_instance

    def extract_restaurant_search(self, user_input: str) -> dict:
        """
        Converts the user input message into a JSON command for restaurant search.
        This is a static method since it doesn't depend on the state of the class.
        """
        prompt = f"""
        Convert the following user message into a JSON command to search for restaurants:
        "{user_input}"

        Only respond with a JSON that matches this format:
        {{
            "action": "restaurant_search",
            "parameters": {{
                "query": "<type of food>",
                "near": "<location>",
                "price": "<price level>",  // optional
                "open_now": <true or false>  // optional
            }}
        }}
        """
        result = self.llm_instance.generate(prompt)
        return result


    @staticmethod
    async def call_foursquare_api(json_command: RestaurantSearch) -> List[Restaurant]:
        """
        Calls the Foursquare API based on the parameters provided in the JSON command.
        Returns a list of Restaurant objects.
        """
        API_URL = "https://api.foursquare.com/v3/places/search"
        HEADERS = {
            "Accept": "application/json",
            "Authorization": f"{Config.FOURSQUARE_KEY}"  # Correct format without 'Bearer'
        }


        # Extract parameters from the LLM response
        params = {
            "query": json_command['parameters'].get('query', 'restaurant'),
            "near": json_command['parameters'].get('near'),
            "open_now": json_command['parameters'].get('open_now', False),
        }
        
        price = json_command['parameters'].get('price')
        if price and price.lower() in price_map:
            params["price"] = price_map[price.lower()]

        # Make the request to Foursquare API
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(API_URL, headers=HEADERS, params=params)
                response.raise_for_status()  # Will raise an error for non-2xx status codes
                data = response.json()

                restaurant_data = []
                results = data.get("results", [])

                # Process the response and extract the required fields
                for item in results:
                    restaurant = Restaurant(
                        name=item.get("name"),
                        address=item["location"].get("formatted_address", "N/A"),
                        cuisine=list(item["features"]["food_and_drink"]["meals"].keys()) 
                                if item.get("features") else [],
                        rating=item.get("rating"),
                        price_level=item.get("price"),
                        hours=["Not Available"] if not item.get("hours") else item.get("hours", {}).get("regular", [])
                    )

                    restaurant_data.append(restaurant)

                return restaurant_data

            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Error fetching data from Foursquare: {e}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
