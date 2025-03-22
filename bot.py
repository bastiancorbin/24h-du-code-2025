import os
from dotenv import load_dotenv

# Import relevant functionality
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool, ToolException
from langchain_core.messages import HumanMessage

from api.client import get_clients, get_client_by_id, create_client, update_client, delete_client
from api.meal import get_meals
from api.reservation import get_reservations, get_reservation_by_id, create_reservation, delete_reservation, update_reservation, update_reservation_with_patch
from api.restaurant import get_restaurants
from api.spas import get_spas


load_dotenv()

os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Tools

search = TavilySearchResults(max_results=2)
tools = [
    search,

    create_client,
    get_clients,
    delete_client,
    get_client_by_id,
    update_client,

    get_meals,

    get_reservations,
    get_reservation_by_id,
    create_reservation,
    delete_reservation,
    update_reservation,
    update_reservation_with_patch,

    get_restaurants,

    get_spas
]

# Config MemorySaver
memory = MemorySaver()
config =  {
    "configurable": {
        "thread_id": "abb123"
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