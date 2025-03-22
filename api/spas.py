from pydantic import BaseModel, Field
from api.api_client import ApiClient
from typing import List

from langchain_core.tools import tool

class Spa(BaseModel):
    id: int = Field(description="The spa's unique identifier")
    name: str = Field(description="The name of the spa")
    description: str = Field(description="A description of the spa")
    location: str = Field(description="The location of the spa")
    phone_number: str = Field(description="The phone number of the spa")
    email: str = Field(description="The email address of the spa")
    opening_hours: str = Field(description="The opening hours of the spa")
    created_at: str = Field(description="The creation timestamp of the spa")
    updated_at: str = Field(description="The last update timestamp of the spa")

class SpaApi:
    def __init__(self):
        self.api_client = ApiClient()
        self.endpoint = "spas"

    @tool
    def get_spas(self) -> List[Spa]:
        """
        Fetches all spa details from the API.

        Returns:
            List[Spa]: A list of Pydantic model instances containing the details of spas.
        """
        try:
            result = self.api_client.get(self.endpoint)
            return [Spa(**spa) for spa in result]  # Convert each item in the list to a Spa instance
        except Exception as e:
            print(f"Error: {e}")
            return []

