import chromadb

def get_chroma_client():
    return chromadb.Client()

def ingest_documents(collection_name: str, documents: list, ids: list) -> dict:
    # STUB VERSION - pretend to store documents
    # Real logic (embedding + upsert) comes later
    return {
        'status': 'success',
        'collection': collection_name,
        'count': len(documents)
    }

def retrieve_documents(collection_name: str, query: str, n_results: int = 3) -> list:
    # STUB VERSION - returns fake retrieved chunks in agreed shape
    return [
        {'doc_id': 'doc_1', 'content': 'Fake retrieved content 1', 'score': 0.91, 'metadata': {'source': 'test'}},
        {'doc_id': 'doc_2', 'content': 'Fake retrieved content 2', 'score': 0.85, 'metadata': {'source': 'test'}}
    ]

if __name__ == '__main__':
    ingest_result = ingest_documents('research_docs', ['doc text 1', 'doc text 2'], ['id1', 'id2'])
    print('Ingest result:', ingest_result)

    retrieve_result = retrieve_documents('research_docs', 'What is LangGraph?')
    print('Retrieve result:', retrieve_result)
