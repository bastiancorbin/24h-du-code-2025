from pydantic import BaseModel, Field
from api.api_client import ApiClient

from langchain_core.tools import tool

class ClientDetail(BaseModel):
    id: int = Field(description="The client's unique identifier")
    name: str = Field(description="The client's name")
    phone_number: str = Field(description="The client's phone number")
    room_number: str | None = Field(description="The client's room number")
    special_requests: str | None = Field(description="Special requests made by the client")

class Client(BaseModel):
    count: int = Field(description="The total number of clients")
    next: str | None = Field(description="The URL to the next page")
    previous: str | None = Field(description="The URL to the previous page")
    results: list[ClientDetail] = Field(description="The list of clients")

class ClientApi:
    def __init__(self):
        self.api_client = ApiClient()
        self.endpoint = "clients"

    @tool
    def get_clients(self, page_number, search) -> Client:
        """
        Get all clients from the API.

        Returns:
            Client: A Pydantic model containing client details.
        """
        try:
            result = self.api_client.get(self.endpoint, params={ "page": page_number, "search": search })
            return Client(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def get_client_by_id(self, client_id: int) -> ClientDetail:
        """
        Get a client by ID from the API.

        Args:
            client_id (int): The unique identifier of the client.

        Returns:
            ClientDetail: A Pydantic model containing client details.
        """
        try:
            result = self.api_client.get(f"{self.endpoint}/{client_id}")
            return ClientDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def create_client(self, name: str, phone_number: str, room_number: str, special_requests: str) -> ClientDetail:
        """
        Create a new client in the API.
        If the client don't give all informations, ask him to give it.

        Args:
            name (str): The client's name.
            phone_number (str): The client's phone number.
            room_number (str): The client's room number.
            special_requests (str): Special requests made by the client.

        Returns:
            ClientDetail: A Pydantic model containing the created client details.
        """
        try:
            result = self.api_client.post(f"{self.endpoint}/", json=
            {
                "name": name,
                "phone_number": phone_number,
                "room_number": room_number,
                "special_requests": special_requests
            })
            return ClientDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def update_client(self, client_id: int, name: str, phone_number: str, room_number: str, special_requests: str) -> ClientDetail:
        """
        Update an existing client in the API.

        Args:
            client_id (int): The unique identifier of the client.
            name (str): The client's name.
            phone_number (str): The client's phone number.
            room_number (str): The client's room number.
            special_requests (str): Special requests made by the client.

        Returns:
            ClientDetail: A Pydantic model containing the updated client details.
        """
        try:
            result = self.api_client.put(f"{self.endpoint}/{client_id}/", json={
                "name": name,
                "phone_number": phone_number,
                "room_number": room_number,
                "special_requests": special_requests
            })
            return ClientDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def delete_client(self, client_id: int) -> None:
        """
        Delete a client by ID from the API.

        Args:
            client_id (int): The unique identifier of the client.

        Returns:
            None
        """
        try:
            self.api_client.delete(f"{self.endpoint}/{client_id}/")
            print(f"Client with ID {client_id} deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
