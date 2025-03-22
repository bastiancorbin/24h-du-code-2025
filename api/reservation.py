from pydantic import BaseModel, Field
from api.api_client import ApiClient

from langchain_core.tools import tool

class ReservationDetail(BaseModel):
    id: int = Field(description="The reservation's unique identifier")
    client: int = Field(description="The ID of the client making the reservation")
    restaurant: int = Field(description="The ID of the restaurant for the reservation")
    date: str = Field(description="The date of the reservation (YYYY-MM-DD)")
    meal: int = Field(description="The ID of the meal type")
    number_of_guests: int = Field(description="The number of guests for the reservation")
    special_requests: str | None = Field(description="Special requests for the reservation")

class Reservation(BaseModel):
    count: int = Field(description="The total number of reservations")
    next: str | None = Field(description="The URL to the next page")
    previous: str | None = Field(description="The URL to the previous page")
    results: list[ReservationDetail] = Field(description="The list of reservations")

class ReservationApi:
    def __init__(self):
        self.api_client = ApiClient()
        self.endpoint = "reservations"

    def get_reservations(self, page_number=None, client_id=None, date_from=None, date_to=None, meal=None, restaurant=None) -> Reservation:
        """
        Get all reservations from the API.

        Args:
            page_number (int, optional): The page number for pagination.
            client_id (int, optional): Filter by client ID.
            date_from (str, optional): Filter by start date (YYYY-MM-DD).
            date_to (str, optional): Filter by end date (YYYY-MM-DD).
            meal (int, optional): Filter by meal type ID.
            restaurant (int, optional): Filter by restaurant ID.

        Returns:
            Reservation: A Pydantic model containing reservation details.
        """
        try:
            params = {
                "page": page_number,
                "client": client_id,
                "date_from": date_from,
                "date_to": date_to,
                "meal": meal,
                "restaurant": restaurant
            }
            result = self.api_client.get(self.endpoint, params={k: v for k, v in params.items() if v is not None})
            return Reservation(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def get_reservation_by_id(self, reservation_id: int) -> ReservationDetail:
        """
        Get a reservation by ID from the API.

        Args:
            reservation_id (int): The unique identifier of the reservation.

        Returns:
            ReservationDetail: A Pydantic model containing reservation details.
        """
        try:
            result = self.api_client.get(f"{self.endpoint}/{reservation_id}")
            return ReservationDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def create_reservation(self, client: int, restaurant: int, date: str, meal: int, number_of_guests: int, special_requests: str | None) -> ReservationDetail:
        """
        Create a new reservation in the API.

        Args:
            client (int): The ID of the client making the reservation.
            restaurant (int): The ID of the restaurant for the reservation.
            date (str): The date of the reservation (YYYY-MM-DD).
            meal (int): The ID of the meal type.
            number_of_guests (int): The number of guests for the reservation.
            special_requests (str, optional): Special requests for the reservation.

        Returns:
            ReservationDetail: A Pydantic model containing the created reservation details.
        """
        try:
            result = self.api_client.post(f"{self.endpoint}/", json={
                "client": client,
                "restaurant": restaurant,
                "date": date,
                "meal": meal,
                "number_of_guests": number_of_guests,
                "special_requests": special_requests
            })
            return ReservationDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def update_reservation(self, reservation_id: int, client: int, restaurant: int, date: str, meal: int, number_of_guests: int, special_requests: str | None) -> ReservationDetail:
        """
        Update an existing reservation in the API.

        Args:
            reservation_id (int): The unique identifier of the reservation.
            client (int): The ID of the client making the reservation.
            restaurant (int): The ID of the restaurant for the reservation.
            date (str): The date of the reservation (YYYY-MM-DD).
            meal (int): The ID of the meal type.
            number_of_guests (int): The number of guests for the reservation.
            special_requests (str, optional): Special requests for the reservation.

        Returns:
            ReservationDetail: A Pydantic model containing the updated reservation details.
        """
        try:
            result = self.api_client.put(f"{self.endpoint}/{reservation_id}/", json={
                "client": client,
                "restaurant": restaurant,
                "date": date,
                "meal": meal,
                "number_of_guests": number_of_guests,
                "special_requests": special_requests
            })
            return ReservationDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def update_reservation_with_patch(self, reservation_id: int, client: int = None, restaurant: int = None, date: str = None, meal: int = None, number_of_guests: int = None, special_requests: str = None) -> ReservationDetail:
        """
        Partially update an existing reservation using PATCH in the API.

        Args:
            reservation_id (int): The unique identifier of the reservation.
            client (int, optional): The ID of the client making the reservation.
            restaurant (int, optional): The ID of the restaurant for the reservation.
            date (str, optional): The date of the reservation (YYYY-MM-DD).
            meal (int, optional): The ID of the meal type.
            number_of_guests (int, optional): The number of guests for the reservation.
            special_requests (str, optional): Special requests for the reservation.

        Returns:
            ReservationDetail: A Pydantic model containing the updated reservation details.
        """
        try:
            updated_data = {
                "client": client,
                "restaurant": restaurant,
                "date": date,
                "meal": meal,
                "number_of_guests": number_of_guests,
                "special_requests": special_requests
            }
            result = self.api_client.patch(f"{self.endpoint}/{reservation_id}/", json={k: v for k, v in updated_data.items() if v is not None})
            return ReservationDetail(**result)
        except Exception as e:
            print(f"Error: {e}")

    @tool
    def delete_reservation(self, reservation_id: int) -> None:
        """
        Delete a reservation by ID from the API.

        Args:
            reservation_id (int): The unique identifier of the reservation.

        Returns:
            None
        """
        try:
            self.api_client.delete(f"{self.endpoint}/{reservation_id}/")
            print(f"Reservation with ID {reservation_id} deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
