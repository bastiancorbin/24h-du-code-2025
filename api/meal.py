from pydantic import BaseModel, Field
from api.api_client import ApiClient

from langchain_core.tools import tool, ToolException

class MealDetail(BaseModel):
    id: int = Field(description="The meal's unique identifier")
    name: str = Field(description="The meal's name")

class Meal(BaseModel):
    count: int = Field(description="The meal's unique identifier")
    next: str | None = Field(description="The URL to the next page")
    previous: str | None = Field(description="The URL to the previous page")
    results: list[MealDetail] = Field(description="The list of meals")

@tool
def get_meals() -> Meal:
    """
    Get all meals.

    Returns:
        Meal: A Pydantic model containing meal details.
    """
    try:
        api_client = ApiClient()
        endpoint = "meals"

        result = api_client.get(endpoint)
        return Meal(**result)
    except Exception as e:
        print(f"Error: {e}")
        raise ToolException(e)
