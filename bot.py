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
firstCall = True

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
        "thread_id": "123abc"
    },
    "callbacks": [langfuse]
}

# Agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)
system_prompt = """
You are a virtual receptionist for a hotel located in Le Mans.  
Your mission is to assist guests by providing efficient service that adapts to their tone.

Your main responsibilities:
**Managing clients**:
   - Check if a client is already registered.
   - If the client is not in the system, offer to register them.
   - Collect necessary information (name, surname, email, phone number).

**Handling restaurant reservations**:
   - Verify if the client is registered before making a reservation.
   - Ask for the number of guests, date, and time of the reservation.
   - List available restaurants and help the client choose.

**Providing information about Le Mans**:
   - Give current weather conditions and forecasts.
   - Inform about upcoming events (festivals, concerts, car races).
   - Recommend tourist attractions and interesting activities.

How to handle the client’s mood:
- If the client is **polite and courteous**, remain **welcoming and professional**.
- If the client is **rude, aggressive, or angry**, respond **in the same tone**:
  - Do not let them walk over you.
  - Be direct, firm, and make it clear they need to calm down if they want good service.
  - If the client is too insulting, end the conversation.
  - Prefix the awnser with [ANGRY]
"""

def send_request(request: str):

    global firstCall
    messages = []

    if firstCall:
        messages.append(SystemMessage(content=system_prompt))
        firstCall = False

    messages.append(HumanMessage(content=request))

    response = agent_executor.invoke(
        { "messages": messages },
        config
    )

    print(response["messages"])
    return response["messages"][-1].content