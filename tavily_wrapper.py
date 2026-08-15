def tavily_search(query: str) -> dict:
    # STUB VERSION - basic search pattern
    return {
        'query': query,
        'results': [
            {'url': 'https://example.com/a', 'title': 'Result A', 'content': 'Fake search content A', 'score': 0.9}
        ]
    }

def tavily_search_with_filter(query: str, domains: list) -> dict:
    # STUB VERSION - domain-filtered search pattern
    return {
        'query': query,
        'domains': domains,
        'results': [
            {'url': 'https://example.com/b', 'title': 'Result B', 'content': 'Fake filtered content', 'score': 0.88}
        ]
    }

def tavily_extract(url: str) -> dict:
    # STUB VERSION - full page extract pattern
    return {
        'url': url,
        'content': 'Fake extracted full page content'
    }

def tavily_multi_query(queries: list) -> list:
    # STUB VERSION - multi-query fan-out pattern
    return [
        {'query': q, 'results': [{'url': 'https://example.com/c', 'title': 'Result C', 'content': 'Fake content', 'score': 0.87}]}
        for q in queries
    ]

if __name__ == '__main__':
    print('Basic search:', tavily_search('LangGraph'))
    print('Filtered search:', tavily_search_with_filter('LangGraph', ['langchain.com']))
    print('Extract:', tavily_extract('https://example.com'))
    print('Multi-query:', tavily_multi_query(['LangGraph', 'ChromaDB']))
