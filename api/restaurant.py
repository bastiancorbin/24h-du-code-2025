from pydantic import BaseModel, Field
from api.api_client import ApiClient

from langchain_core.tools import tool

class RestaurantDetail(BaseModel):
    id: int = Field(description="The restaurant's unique identifier")
    name: str = Field(description="The restaurant's name")
    description: str = Field(description="The restaurant's description")
    capacity: int = Field(description="The restaurant's capacity")
    opening_hours: str = Field(description="The restaurant's opening hours")
    location: str = Field(description="The restaurant's location")
    is_active: bool = Field(description="Whether the restaurant is active")

class Restaurant(BaseModel):
    count: int = Field(description="The total number of restaurants")
    next: str | None = Field(description="The URL to the next page")
    previous: str | None = Field(description="The URL to the previous page")
    results: list[RestaurantDetail] = Field(description="The list of restaurants")

@tool
def get_restaurants(page_number: int = 1) -> Restaurant:
    """
    Get all restaurants.

    Args:
        page_number (int): The page number for pagination.

    Returns:
        Restaurant: A Pydantic model containing restaurant details.
    """
    try:
        api_client = ApiClient()
        endpoint = "restaurants"

        result = api_client.get(endpoint, params={"page": page_number})
        return Restaurant(**result)
    except Exception as e:
        print(f"Error: {e}")
