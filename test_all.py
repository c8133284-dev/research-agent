from research_agent import research_agent, dedup_sources, expand_query
from chromadb_service import ingest_documents, retrieve_documents
from vector_store_utils import get_stats

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        print(f'PASS: {name}')
        passed += 1
    else:
        print(f'FAIL: {name}')
        failed += 1

print('--- Testing expand_query ---')
check('expand_query returns 3 variations', len(expand_query('LangGraph')) == 3)
check('expand_query handles empty string', expand_query('') == [])

print('--- Testing dedup_sources ---')
sample = [
    {'url': 'https://a.com', 'title': 'A'},
    {'url': 'https://a.com', 'title': 'A duplicate'},
    {'url': 'https://b.com', 'title': 'B'}
]
result = dedup_sources(sample)
check('dedup_sources removes duplicate URLs', len(result) == 2)

print('--- Testing research_agent ---')
result = research_agent('What is ChromaDB?')
check('research_agent returns sources', len(result['sources']) > 0)
check('research_agent returns reranked_results', len(result['reranked_results']) > 0)
check('research_agent handles empty query', research_agent('')['error'] == 'empty_query')

print('--- Testing chromadb_service ---')
ingest_result = ingest_documents('test_collection', ['Sample test document about AI'], ['test_id_1'])
check('ingest_documents succeeds', ingest_result['status'] == 'success')

retrieve_result = retrieve_documents('test_collection', 'AI document')
check('retrieve_documents returns results', len(retrieve_result) > 0)

mismatch_result = ingest_documents('test_collection', ['doc1', 'doc2'], ['id1'])
check('ingest_documents catches mismatched lengths', mismatch_result['status'] == 'error')

print('--- Testing vector_store_utils ---')
stats = get_stats('test_collection')
check('get_stats returns document_count', 'document_count' in stats)

print()
print(f'RESULTS: {passed} passed, {failed} failed')
