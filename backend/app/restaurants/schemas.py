from pydantic import BaseModel
from typing import Optional, List, Union


class RestaurantParams(BaseModel):
    query: str
    near: str
    price: Optional[str] = None
    open_now: Optional[bool] = False


class RestaurantSearch(BaseModel):
    action: str
    parameters: RestaurantParams


class Restaurant(BaseModel):
    name: str
    address: str
    cuisine: List[str] = []
    rating: Optional[float] = None
    price_level: Optional[int] = None
    hours: Union[List[str], str] = "Not Available" 

class UserQuery(BaseModel):
    message: str
