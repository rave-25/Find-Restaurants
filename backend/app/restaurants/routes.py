
from fastapi import  HTTPException, APIRouter
from app.restaurants.schemas import UserQuery
from .service import get_llm_json_command, call_foursquare_api

restaurant_router = APIRouter()

@restaurant_router.post('/execute')
async def find_restaurants(user_message: UserQuery):
    # Step 1: Send the user's message to OpenAI to generate the JSON command
    llm_response = await get_llm_json_command(user_message.message)
    print("LLM Response:", llm_response)
    if not llm_response:
        raise HTTPException(status_code=400, detail="Failed to generate valid JSON from LLM.")

    # Step 2: Use the parsed JSON to make an API call to Foursquare
    restaurants = await call_foursquare_api(llm_response)

    if not restaurants:
        raise HTTPException(status_code=500, detail="Error fetching data from Foursquare.")

    # Step 3: Return the restaurant results to the user
    return {"restaurants": restaurants}