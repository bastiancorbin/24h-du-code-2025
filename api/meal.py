from pydantic import BaseModel, Field
from api.api_client import ApiClient

from langchain_core.tools import tool

class MealDetail(BaseModel):
    id: int = Field(description="The meal's unique identifier")
    name: str = Field(description="The meal's name")

class Meal(BaseModel):
    count: int = Field(description="The meal's unique identifier")
    next: str | None = Field(description="The URL to the next page")
    previous: str | None = Field(description="The URL to the previous page")
    results: list[MealDetail] = Field(description="The list of meals")

class MealApi:
    def __init__(self):
        self.api_client = ApiClient()
        self.endpoint = "meals"

    @tool
    def get_meals(self) -> Meal:
        """
        Get all meals from the API.

        Returns:
            Meal: A Pydantic model containing meal details.
        """
        try:
            result = self.api_client.get(self.endpoint)
            return Meal(**result)
        except Exception as e:
            print(f"Error: {e}")
