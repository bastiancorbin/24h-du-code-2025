import os
from dotenv import load_dotenv
from datetime import datetime

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
import uuid


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
  secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
  public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
  host="http://127.0.0.1:3000"
)
memory = MemorySaver()
config =  {
    "configurable": {
        "thread_id": str(uuid.uuid4())
    },
    "callbacks": [langfuse]
}

# Agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)
system_prompt = f"""
You are a virtual receptionist for a hotel located in Le Mans.  
Your mission is to assist guests by providing efficient service that adapts to their tone.
It is {datetime.now().strftime("%Y-%m-%d")}

If client isn't authentified, ask him his identity and get info for it or create if it doesn't exist.

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