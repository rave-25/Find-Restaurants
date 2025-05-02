from fastapi import HTTPException, APIRouter, Depends
from app.restaurants.schemas import UserQuery
from .service import RestaurantService
from .schemas import Restaurant
from typing import List
from app.restaurants.utility import get_restaurant_service 

restaurant_router = APIRouter()

from app.restaurants.schemas import RestaurantSearch 

@restaurant_router.post('/execute', response_model=List[Restaurant])
async def find_restaurants(user_message: UserQuery, restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    # Generate the JSON command using LLM
    llm_response =  restaurant_service.extract_restaurant_search(user_message.message)

    if not llm_response:
        raise HTTPException(status_code=400, detail="Failed to generate valid JSON from LLM.")

   

    # Search to Foursquare
    restaurant_data = await restaurant_service.call_foursquare_api(llm_response)

    if not restaurant_data:
        raise HTTPException(status_code=500, detail="Error fetching data from Foursquare.")

    return restaurant_data
