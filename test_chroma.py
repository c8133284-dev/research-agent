import chromadb

client = chromadb.Client()
collection = client.create_collection('test')
collection.add(documents=['hello world'], ids=['1'])
result = collection.query(query_texts=['hello'], n_results=1)
print(result)
