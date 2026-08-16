'''
tavily_wrapper.py
Owns: Tavily integration (P2)
Responsibility: wrap all Tavily API calls with retry/backoff so
transient failures (timeouts, rate limits) don't crash the pipeline.
Implements 4 patterns: basic search, filtered search, page extraction,
and multi-query fan-out.
'''

import os
import time
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))


def with_retry(func, max_retries=3, base_delay=2):
    '''
    Runs func() and retries on failure with exponential backoff
    (waits 2s, then 4s, then 8s between attempts).
    Returns None if every attempt fails, instead of raising.
    '''
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                print(f'Failed after {max_retries} attempts: {e}')
                return None
            wait_time = base_delay * (2 ** (attempt - 1))
            print(f'Attempt {attempt} failed ({e}). Retrying in {wait_time}s...')
            time.sleep(wait_time)


def tavily_search(query: str) -> dict:
    '''Pattern 1: basic search - returns ranked results for a single query.'''
    def call():
        response = client.search(query)
        results = [
            {'url': r['url'], 'title': r['title'], 'content': r['content'], 'score': r['score']}
            for r in response['results']
        ]
        return {'query': query, 'results': results}

    result = with_retry(call)
    if result is None:
        return {'query': query, 'results': [], 'error': 'search_failed'}
    return result


def tavily_search_with_filter(query: str, domains: list) -> dict:
    '''Pattern 2: domain-filtered search - restricts results to trusted sources.'''
    def call():
        response = client.search(query, include_domains=domains)
        results = [
            {'url': r['url'], 'title': r['title'], 'content': r['content'], 'score': r['score']}
            for r in response['results']
        ]
        return {'query': query, 'domains': domains, 'results': results}

    result = with_retry(call)
    if result is None:
        return {'query': query, 'domains': domains, 'results': [], 'error': 'search_failed'}
    return result


def tavily_extract(url: str) -> dict:
    '''Pattern 3: full page extraction - gets complete content beyond the search snippet.'''
    def call():
        response = client.extract(urls=[url])
        content = response['results'][0]['raw_content'] if response['results'] else ''
        return {'url': url, 'content': content}

    result = with_retry(call)
    if result is None:
        return {'url': url, 'content': '', 'error': 'extract_failed'}
    return result


def tavily_multi_query(queries: list) -> list:
    '''Pattern 4: multi-query fan-out - runs several searches and returns all results together.'''
    return [tavily_search(q) for q in queries]


if __name__ == '__main__':
    print('Testing search with retry wrapper...')
    result = tavily_search('What is LangGraph?')
    print('Success! Got', len(result['results']), 'results')
