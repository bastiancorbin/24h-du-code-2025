import os
from dotenv import load_dotenv

# Import relevant functionality
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool, ToolException
from langchain_core.messages import HumanMessage

from api.client import ClientApi
from api.meal import MealApi
from api.reservation import ReservationApi
from api.restaurant import RestaurantApi
from api.spas import SpaApi


load_dotenv()

os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Tools

client = ClientApi()
meal = MealApi()
reservation = ReservationApi()
restaurant = RestaurantApi()
spa = SpaApi()

search = TavilySearchResults(max_results=2)
tools = [
    search,

    client.create_client,
    client.get_clients,
    client.delete_client,
    client.get_client_by_id,
    client.update_client,

    meal.get_meals,

    reservation.get_reservations,
    reservation.get_reservation_by_id,
    reservation.create_reservation,
    reservation.delete_reservation,
    reservation.update_reservation,
    reservation.update_reservation_with_patch,

    restaurant.get_restaurants,

    spa.get_spas
]

# Config MemorySaver
memory = MemorySaver()
config =  {
    "configurable": {
        "thread_id": "abc123"
    }
}

# Agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)

def send_request(request: str):

    response = agent_executor.invoke(
        {
            "messages": [HumanMessage(content=request)]
        },
        config
    )

    print(response["messages"])
    return response["messages"][1].content