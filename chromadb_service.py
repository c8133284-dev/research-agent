import chromadb

client = chromadb.PersistentClient(path='./chroma_data')

def get_chroma_client():
    return client

def ingest_documents(collection_name: str, documents: list, ids: list) -> dict:
    if not collection_name or not collection_name.strip():
        return {'status': 'error', 'error': 'missing_collection_name'}

    if not documents or not ids:
        return {'status': 'error', 'error': 'empty_documents_or_ids'}

    if len(documents) != len(ids):
        return {'status': 'error', 'error': 'documents_ids_length_mismatch'}

    try:
        collection = client.get_or_create_collection(collection_name)
        collection.add(documents=documents, ids=ids)
        return {
            'status': 'success',
            'collection': collection_name,
            'count': len(documents)
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def retrieve_documents(collection_name: str, query: str, n_results: int = 3) -> list:
    if not collection_name or not query or not query.strip():
        return []

    try:
        collection = client.get_or_create_collection(collection_name)
        results = collection.query(query_texts=[query], n_results=n_results)

        ids = results.get('ids', [[]])[0]
        docs = results.get('documents', [[]])[0]
        distances = results.get('distances', [[]])[0]

        if not ids:
            return []

        output = []
        for i in range(len(ids)):
            output.append({
                'doc_id': ids[i],
                'content': docs[i] if i < len(docs) else '',
                'score': distances[i] if i < len(distances) else None,
                'metadata': {}
            })
        return output
    except Exception as e:
        print(f'Retrieve failed: {e}')
        return []

if __name__ == '__main__':
    print('Testing normal ingest...')
    result = ingest_documents('research_docs', ['Test doc for error handling'], ['err_test_1'])
    print(result)

    print('Testing mismatched lengths...')
    result2 = ingest_documents('research_docs', ['doc1', 'doc2'], ['id1'])
    print(result2)

    print('Testing empty query retrieve...')
    result3 = retrieve_documents('research_docs', '')
    print(result3)

    print('Testing normal retrieve...')
    result4 = retrieve_documents('research_docs', 'test document')
    print('Got', len(result4), 'results')
