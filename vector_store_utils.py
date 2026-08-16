'''
vector_store_utils.py
Owns: Vector store maintenance utilities (P2)
Responsibility: initialize collections, report stats, and manage
the lifecycle (delete/reset) of the persistent ChromaDB store.
'''

import chromadb

client = chromadb.PersistentClient(path='./chroma_data')


def init_vector_store(collection_name: str) -> dict:
    '''Creates the collection if it doesn't exist yet, or confirms it does.'''
    collection = client.get_or_create_collection(collection_name)
    return {'status': 'initialized', 'collection': collection_name}


def get_stats(collection_name: str) -> dict:
    '''Returns how many documents are currently stored in a collection.'''
    collection = client.get_or_create_collection(collection_name)
    count = collection.count()
    return {'collection': collection_name, 'document_count': count}


def delete_documents(collection_name: str, ids: list) -> dict:
    '''Deletes specific documents from a collection by their ids.'''
    if not ids:
        return {'status': 'error', 'error': 'no_ids_provided'}
    collection = client.get_or_create_collection(collection_name)
    collection.delete(ids=ids)
    return {'status': 'deleted', 'collection': collection_name, 'deleted_count': len(ids)}


def reset_collection(collection_name: str) -> dict:
    '''Wipes a collection completely and recreates it empty. Use with care.'''
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass  # collection may not have existed yet - that's fine
    client.create_collection(collection_name)
    return {'status': 'reset', 'collection': collection_name}


if __name__ == '__main__':
    print('Init:', init_vector_store('research_docs'))
    print('Stats:', get_stats('research_docs'))
