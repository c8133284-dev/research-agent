import chromadb

client = chromadb.PersistentClient(path='./chroma_data')

def init_vector_store(collection_name: str) -> dict:
    collection = client.get_or_create_collection(collection_name)
    return {'status': 'initialized', 'collection': collection_name}

def get_stats(collection_name: str) -> dict:
    collection = client.get_or_create_collection(collection_name)
    count = collection.count()
    return {'collection': collection_name, 'document_count': count}

def delete_documents(collection_name: str, ids: list) -> dict:
    collection = client.get_or_create_collection(collection_name)
    collection.delete(ids=ids)
    return {'status': 'deleted', 'collection': collection_name, 'deleted_count': len(ids)}

def reset_collection(collection_name: str) -> dict:
    client.delete_collection(collection_name)
    client.create_collection(collection_name)
    return {'status': 'reset', 'collection': collection_name}

if __name__ == '__main__':
    init_vector_store('research_docs')
    print('Ingesting a test doc...')
    collection = client.get_or_create_collection('research_docs')
    collection.add(documents=['LangGraph is an agent framework.'], ids=['persist_test_1'])
    print('Stats:', get_stats('research_docs'))
