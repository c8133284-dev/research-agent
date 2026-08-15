from tavily import TavilyClient

client = TavilyClient(api_key="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")
result = client.search("What is LangChain?")
print(result)