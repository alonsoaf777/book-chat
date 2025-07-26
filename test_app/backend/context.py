import pandas as pd
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import os

# Global encoder and qdrant setup
encoder = SentenceTransformer('all-MiniLM-L6-v2')
qdrant = QdrantClient(":memory:")

# Prepare data
wd_PATH = os.getcwd()
data_PATH = r"D:\home\[00]_Projects\LLMs\DataEngineering\vector-DB\data\RAG_df2.csv"
df = pd.read_csv(data_PATH, skipinitialspace=True, engine='python', encoding= "UTF-8")
data = df.sample(1000).to_dict('records') #small sample

# Collection index
def index_data(collection_name):
    # Calculate the embeddings of the requested data
    vectors = encoder.encode([combine_fields(doc) for doc in data]).tolist()

    # Create a qdrant collection
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )

    # Upload points using the embeddins
    qdrant.upload_points(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=idx,
                vector=vector,
                payload=doc
            )
            for idx, (vector, doc) in enumerate(zip(vectors, data))
        ]
    )
    print(f"Indexed {len(data)} books into collection '{collection_name}'.")

# 3Función de búsqueda
def get_context(user_prompt: str):
    #Encode the prompt
    query_vector = encoder.encode(user_prompt).tolist()

    hits = qdrant.search(
        collection_name= "books",
        query_vector=query_vector,
        limit=3 #Just use top 3 samples based on hit percentage
    )

    return [hit.payload for hit in hits]

def combine_fields(doc):
    return (
        f"Title: {doc['title']}. "
        f"Author: {doc['author']}. "
        f"Year: {doc['year']}. "
        f"Description: {doc['description']}. "
        f"Pages: {doc['pages']}. "
        f"Genres: {doc['genres']}. "
        f"Rating: {doc['rating']}."
    )