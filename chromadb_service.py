'''
chromadb_service.py
Owns: ChromaDB Service (P2)
Responsibility: ingest documents into a persistent vector store and
retrieve the most semantically relevant documents for a given query.
'''

import chromadb
from datetime import datetime

# PersistentClient saves data to disk (./chroma_data) so it survives
# between separate script runs - unlike the default in-memory Client.
client = chromadb.PersistentClient(path='./chroma_data')


def get_chroma_client():
    '''Returns the shared ChromaDB client instance.'''
    return client


def ingest_documents(collection_name: str, documents: list, ids: list) -> dict:
    '''
    Embeds and stores a list of documents in the given collection.
    Each document is tagged with an 'ingested_at' timestamp in its metadata,
    so later retrieval can show when the info was added.

    Validates inputs first (missing name, empty lists, mismatched lengths)
    so bad calls fail with a clear error instead of an unhandled exception.
    '''
    if not collection_name or not collection_name.strip():
        return {'status': 'error', 'error': 'missing_collection_name'}

    if not documents or not ids:
        return {'status': 'error', 'error': 'empty_documents_or_ids'}

    if len(documents) != len(ids):
        return {'status': 'error', 'error': 'documents_ids_length_mismatch'}

    try:
        collection = client.get_or_create_collection(collection_name)
        timestamp = datetime.now().isoformat()
        metadatas = [{'ingested_at': timestamp} for _ in documents]
        collection.add(documents=documents, ids=ids, metadatas=metadatas)
        return {
            'status': 'success',
            'collection': collection_name,
            'count': len(documents)
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


def retrieve_documents(collection_name: str, query: str, n_results: int = 3) -> list:
    '''
    Searches the given collection for documents most similar to the query.
    Returns a list of {doc_id, content, score, metadata} dicts, sorted by
    relevance (lower score = more similar, since ChromaDB returns distance).
    Returns an empty list on any failure or if there's nothing to find.
    '''
    if not collection_name or not query or not query.strip():
        return []

    try:
        collection = client.get_or_create_collection(collection_name)
        results = collection.query(query_texts=[query], n_results=n_results)

        ids = results.get('ids', [[]])[0]
        docs = results.get('documents', [[]])[0]
        distances = results.get('distances', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]

        if not ids:
            return []

        output = []
        for i in range(len(ids)):
            output.append({
                'doc_id': ids[i],
                'content': docs[i] if i < len(docs) else '',
                'score': distances[i] if i < len(distances) else None,
                'metadata': metadatas[i] if i < len(metadatas) and metadatas[i] else {}
            })
        return output
    except Exception as e:
        print(f'Retrieve failed: {e}')
        return []


if __name__ == '__main__':
    print('Testing ingest with metadata...')
    result = ingest_documents('research_docs', ['Polished test document'], ['polish_test_1'])
    print(result)

    print('Testing retrieve shows metadata...')
    retrieved = retrieve_documents('research_docs', 'Polished test')
    print(retrieved)
