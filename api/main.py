from langchain_core.tools import StructuredTool, tool
from spas import SpaApi

spa = SpaApi()

tool = StructuredTool.from_function(func=spa.get_spas)

response = tool.invoke({})

if response:
    print(response)