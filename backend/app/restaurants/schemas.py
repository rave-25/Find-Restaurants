from pydantic import BaseModel
from typing import Optional, List


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
    cuisine: str
    rating: Optional[float] = None
    price_level: Optional[str] = None
    hours: Optional[str] = None

class UserQuery(BaseModel):
    message: str
