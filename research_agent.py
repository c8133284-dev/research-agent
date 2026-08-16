'''
research_agent.py
Owns: Research Agent (P2)
Responsibility: expand a user query, fan out to Tavily, remove duplicate
sources, and rank remaining sources by relevance score.
'''

from tavily_wrapper import tavily_search


def expand_query(query: str) -> list:
    '''
    Turns one query into several variations to improve search coverage.
    Example: 'LangGraph' -> ['LangGraph', 'LangGraph explained', 'LangGraph tutorial']
    Returns an empty list if the query is blank.
    '''
    if not query or not query.strip():
        return []
    return [
        query,
        f'{query} explained',
        f'{query} tutorial'
    ]


def dedup_sources(sources: list) -> list:
    '''
    Removes duplicate sources by URL.
    If the same URL appears more than once (common when searching multiple
    query variations), keeps only the copy with the highest relevance score.
    '''
    best_by_url = {}
    for s in sources:
        url = s.get('url')
        if not url:
            continue
        current_score = s.get('score', 0)
        if url not in best_by_url or current_score > best_by_url[url].get('score', 0):
            best_by_url[url] = s
    return list(best_by_url.values())


def research_agent(query: str) -> dict:
    '''
    Main entry point for the Research Agent.

    Steps:
      1. Expand the query into multiple variations
      2. Search Tavily for each variation
      3. Remove duplicate sources (keeping the best-scoring copy)
      4. Rank remaining sources by relevance score, highest first

    Returns a dict with the original query, the list of unique sources,
    and a separately ranked list of {url, score} pairs.
    On failure (empty query or no results found), returns an 'error' key
    instead of raising an exception, so the pipeline never crashes here.
    '''
    if not query or not query.strip():
        return {'query': query, 'sources': [], 'reranked_results': [], 'error': 'empty_query'}

    expanded_queries = expand_query(query)

    all_sources = []
    for q in expanded_queries:
        result = tavily_search(q)
        if result.get('error'):
            # One failed search shouldn't stop the others - just skip it
            continue
        all_sources.extend(result.get('results', []))

    if not all_sources:
        return {'query': query, 'sources': [], 'reranked_results': [], 'error': 'no_results_found'}

    unique_sources = dedup_sources(all_sources)

    sources_formatted = [
        {'url': s.get('url', ''), 'title': s.get('title', ''), 'content': s.get('content', '')}
        for s in unique_sources
    ]

    reranked = sorted(unique_sources, key=lambda x: x.get('score', 0), reverse=True)
    reranked_formatted = [
        {'url': r.get('url', ''), 'score': r.get('score', 0)}
        for r in reranked
    ]

    return {
        'query': query,
        'sources': sources_formatted,
        'reranked_results': reranked_formatted
    }


if __name__ == '__main__':
    print('Testing normal query...')
    result = research_agent('What is LangGraph?')
    print('Got', len(result['sources']), 'sources')

    print('Testing empty query...')
    print(research_agent(''))
