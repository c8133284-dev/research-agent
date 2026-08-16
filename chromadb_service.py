import chromadb

client = chromadb.PersistentClient(path='./chroma_data')

def get_chroma_client():
    return client

def ingest_documents(collection_name: str, documents: list, ids: list) -> dict:
    collection = client.get_or_create_collection(collection_name)
    collection.add(documents=documents, ids=ids)
    return {
        'status': 'success',
        'collection': collection_name,
        'count': len(documents)
    }

def retrieve_documents(collection_name: str, query: str, n_results: int = 3) -> list:
    collection = client.get_or_create_collection(collection_name)
    results = collection.query(query_texts=[query], n_results=n_results)

    output = []
    ids = results['ids'][0]
    docs = results['documents'][0]
    distances = results['distances'][0]
    for i in range(len(ids)):
        output.append({
            'doc_id': ids[i],
            'content': docs[i],
            'score': distances[i],
            'metadata': {}
        })
    return output

if __name__ == '__main__':
    stats_before = get_chroma_client().get_or_create_collection('research_docs').count()
    print('Documents before:', stats_before)

    retrieve_result = retrieve_documents('research_docs', 'What is LangGraph?')
    print('Retrieve result:', retrieve_result)
