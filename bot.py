import os
from dotenv import load_dotenv

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

model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Tools
search = TavilySearchResults(max_results=2)
tools = [search]

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

    # response = agent_executor.invoke(
    #     {
    #         "messages": [HumanMessage(content=request)]
    #     },
    #     config
    # )

    # return response["messages"]

    return "Le bot envoie un truc"  