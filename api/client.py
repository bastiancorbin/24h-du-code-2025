from pydantic import BaseModel, Field
from api.api_client import ApiClient

from langchain_core.tools import tool, ToolException

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

@tool
def get_clients(page_number, search) -> Client:
    """
    Search for clients.

    Returns:
        Client: A Pydantic model containing client details.
    """
    try:
        api_client = ApiClient()
        endpoint = "clients"

        result = api_client.get(endpoint, params={ "page": page_number, "search": search })
        return Client(**result)
    except Exception as e:
        print(f"Error: {e}")
        raise ToolException(e)

@tool
def get_client_by_id(client_id: int) -> ClientDetail:
    """
    Get a client by ID.
    To get the Id you have to search the client first.

    Args:
        client_id (int): The unique identifier of the client.

    Returns:
        ClientDetail: A Pydantic model containing client details.
    """
    try:
        api_client = ApiClient()
        endpoint = "clients"

        result = api_client.get(f"{endpoint}/{client_id}")
        return ClientDetail(**result)
    except Exception as e:
        print(f"Error: {e}")
        raise ToolException(e)

@tool
def create_client(name: str, phone_number: str, room_number: str, special_requests: str="") -> ClientDetail:
    """
    Create a new client.
    If the client don't give all informations, ask him to give it.
    Ensure the room_number is not already taken (available by listing clients).

    Args:
        name (str): The client's name.
        phone_number (str): The client's phone number.
        room_number (str): The client's room number.
        special_requests (str): Special requests made by the client.

    Returns:
        ClientDetail: A Pydantic model containing the created client details.
    """
    try:
        api_client = ApiClient()
        endpoint = "clients"

        result = api_client.post(f"{endpoint}/", json=
        {
            "name": name,
            "phone_number": phone_number,
            "room_number": room_number,
            "special_requests": special_requests
        })
        return ClientDetail(**result)
    except Exception as e:
        print(f"Error: {e}")
        raise ToolException(e)

@tool
def update_client(client_id: int, name: str, phone_number: str, room_number: str, special_requests: str="") -> ClientDetail:
    """
    Update an existing client.
    Get the client ID for update it.
    If client want to change his room number, just increment it or search in special request if he notified a special room.

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
        api_client = ApiClient()
        endpoint = "clients"

        result = api_client.put(f"{endpoint}/{client_id}/", json={
            "name": name,
            "phone_number": phone_number,
            "room_number": room_number,
            "special_requests": special_requests
        })
        return ClientDetail(**result)
    except Exception as e:
        print(f"Error: {e}")
        raise ToolException(e)

@tool
def delete_client(client_id: int) -> None:
    """
    Delete a client by ID.
    Get the client ID for delete it.
    Call this method when the client leave the hotel (or gave back the keys).

    Args:
        client_id (int): The unique identifier of the client.

    Returns:
        None
    """
    try:
        api_client = ApiClient()
        endpoint = "clients"

        api_client.delete(f"{endpoint}/{client_id}/")
        print(f"Client with ID {client_id} deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise ToolException(e)
