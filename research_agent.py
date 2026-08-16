from tavily_wrapper import tavily_search

def expand_query(query: str) -> list:
    if not query or not query.strip():
        return []
    return [
        query,
        f'{query} explained',
        f'{query} tutorial'
    ]

def dedup_sources(sources: list) -> list:
    seen_urls = set()
    unique = []
    for s in sources:
        url = s.get('url')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(s)
    return unique

def research_agent(query: str) -> dict:
    if not query or not query.strip():
        return {'query': query, 'sources': [], 'reranked_results': [], 'error': 'empty_query'}

    expanded_queries = expand_query(query)

    all_sources = []
    for q in expanded_queries:
        result = tavily_search(q)
        if result.get('error'):
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
    result2 = research_agent('')
    print(result2)
