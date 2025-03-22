import os
from dotenv import load_dotenv

# Import relevant functionality
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool, ToolException
from langchain_core.messages import SystemMessage, HumanMessage
from langfuse.callback import CallbackHandler

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

search = TavilySearchResults(
    max_results=2
)

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
langfuse = CallbackHandler(
  secret_key="sk-lf-f3cf6da2-97e7-401d-bf20-e44b47c34026",
  public_key="pk-lf-b854d47a-a949-434b-b1b1-9580bbe6df0c",
  host="http://10.110.10.172:3000"
)
memory = MemorySaver()
config =  {
    "configurable": {
        "thread_id": "abb123"
    },
    "callbacks": [langfuse]
}

# Agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)
system_prompt = """


"""

def send_request(request: str):

    response = agent_executor.invoke(
        {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=request)
            ]
        },
        config
    )

    print(response["messages"])
    return response["messages"][-1].content