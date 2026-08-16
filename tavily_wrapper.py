import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

def tavily_search(query: str) -> dict:
    # REAL VERSION - actual Tavily API call
    response = client.search(query)
    results = [
        {'url': r['url'], 'title': r['title'], 'content': r['content'], 'score': r['score']}
        for r in response['results']
    ]
    return {'query': query, 'results': results}

def tavily_search_with_filter(query: str, domains: list) -> dict:
    # REAL VERSION - domain-filtered search
    response = client.search(query, include_domains=domains)
    results = [
        {'url': r['url'], 'title': r['title'], 'content': r['content'], 'score': r['score']}
        for r in response['results']
    ]
    return {'query': query, 'domains': domains, 'results': results}

def tavily_extract(url: str) -> dict:
    # REAL VERSION - extract full page content
    response = client.extract(urls=[url])
    content = response['results'][0]['raw_content'] if response['results'] else ''
    return {'url': url, 'content': content}

def tavily_multi_query(queries: list) -> list:
    # REAL VERSION - fan out multiple queries
    return [tavily_search(q) for q in queries]

if __name__ == '__main__':
    print('Basic search:', tavily_search('LangGraph'))
