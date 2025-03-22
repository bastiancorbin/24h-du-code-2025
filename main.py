from ApiClient import ApiClient
import os
from dotenv import load_dotenv
from typing import Annotated, List

# Import relevant functionality
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool, ToolException
from langchain_core.messages import HumanMessage

load_dotenv()

os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

memory = MemorySaver()
model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Tools
search = TavilySearchResults(max_results=2)

@tool
def search_for_clients(
    search: Annotated[str, "search query"], 
    page: Annotated[int, "page number of the search results (start from 1)"]
) -> dict:
    """Search for client in the hotel database"""

    try:
        api_client = ApiClient()
        response = api_client.call_api("clients", {"search": search, "page": page})

        return response
    except Exception as e:
        raise ToolException(f"Error while searching for clients: {e}")
    

tools = [search_for_clients]

# Agent
config =  {
    "configurable": {
        "thread_id": "abc123"
    }
}
agent_executor = create_react_agent(model, tools, checkpointer=memory)

response = agent_executor.invoke(
    {
        "messages": [HumanMessage(content="Search for clients that have phone number starting with 06")]
    },
    config
)

print(response["messages"])