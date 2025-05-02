

import asyncio
from app.restaurants.service import RestaurantService
from app.restaurants.schemas import UserQuery  # your Pydantic model

restaurant_servce = RestaurantService()
async def test_llm_pipeline():
    # Step 1: Simulate user input
    user_message = UserQuery(message="Find Italian restaurants in New York with outdoor seating")

    # Step 2: Get LLM JSON
    llm_response =  restaurant_servce.extract_restaurant_search(user_message.message)
    print("LLM Response:", llm_response)

    if not llm_response:
        print("Failed to generate valid JSON from LLM.")
        return



# Run it
if __name__ == "__main__":
    asyncio.run(test_llm_pipeline())
