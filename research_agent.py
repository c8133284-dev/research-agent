def research_agent(query: str) -> dict:
    # STUB VERSION - returns fake data in the agreed shape
    # Real logic (Tavily search + ranking) comes later
    return {
        'query': query,
        'sources': [
            {'url': 'https://example.com/1', 'title': 'Example Source 1', 'content': 'Fake content for testing'},
            {'url': 'https://example.com/2', 'title': 'Example Source 2', 'content': 'Fake content for testing'}
        ],
        'reranked_results': [
            {'url': 'https://example.com/1', 'score': 0.95}
        ]
    }

if __name__ == '__main__':
    result = research_agent('What is LangGraph?')
    print(result)
