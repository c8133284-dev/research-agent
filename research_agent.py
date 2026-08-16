from tavily_wrapper import tavily_search

def expand_query(query: str) -> list:
    # Simple expansion - creates variations of the query
    return [
        query,
        f'{query} explained',
        f'{query} tutorial'
    ]

def dedup_sources(sources: list) -> list:
    # Remove duplicate URLs
    seen_urls = set()
    unique = []
    for s in sources:
        if s['url'] not in seen_urls:
            seen_urls.add(s['url'])
            unique.append(s)
    return unique

def research_agent(query: str) -> dict:
    expanded_queries = expand_query(query)

    all_sources = []
    for q in expanded_queries:
        result = tavily_search(q)
        all_sources.extend(result['results'])

    unique_sources = dedup_sources(all_sources)

    sources_formatted = [
        {'url': s['url'], 'title': s['title'], 'content': s['content']}
        for s in unique_sources
    ]

    reranked = sorted(unique_sources, key=lambda x: x['score'], reverse=True)
    reranked_formatted = [
        {'url': r['url'], 'score': r['score']}
        for r in reranked
    ]

    return {
        'query': query,
        'sources': sources_formatted,
        'reranked_results': reranked_formatted
    }

if __name__ == '__main__':
    result = research_agent('What is LangGraph?')
    print('Number of unique sources:', len(result['sources']))
    print(result)
