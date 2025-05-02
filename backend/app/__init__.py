from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .restaurants.routes import restaurant_router
from app.restaurants.service import RestaurantService
from app.restaurants.utility import get_restaurant_service


version = "v1"
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restaurant_router, prefix="/api/v1", tags=["restaurants"])


