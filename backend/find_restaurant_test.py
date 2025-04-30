

import asyncio
from app.restaurants.service import get_llm_json_command, call_foursquare_api   # adjust this import if needed
 # adjust this import if needed
from app.restaurants.schemas import UserQuery  # your Pydantic model

async def test_llm_pipeline():
    # Step 1: Simulate user input
    user_message = UserQuery(message="Find Italian restaurants in New York with outdoor seating")

    # Step 2: Get LLM JSON
    llm_response = await get_llm_json_command(user_message.message)
    print("LLM Response:", llm_response)

    if not llm_response:
        print("❌ Failed to generate valid JSON from LLM. hdbdd")
        return

    # Step 3: Call Foursquare API using LLM output
    try:
        restaurants = await call_foursquare_api(llm_response)
        print("✅ Restaurants found:", restaurants)
    except Exception as e:
        print("❌ Error calling Foursquare API:", str(e))

# Run it
if __name__ == "__main__":
    asyncio.run(test_llm_pipeline())
