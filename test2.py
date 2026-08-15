from dotenv import load_dotenv
import os
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv('TAVILY_API_KEY')
client = TavilyClient(api_key=api_key)
result = client.search('What is ChromaDB?')
print(result)
