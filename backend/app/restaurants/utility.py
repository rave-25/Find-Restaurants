from app.llm.llm import HuggingFaceLLM
from app.restaurants.service import RestaurantService

def get_restaurant_service() -> RestaurantService:
    llm_instance = HuggingFaceLLM() 
    return RestaurantService(llm_instance)
