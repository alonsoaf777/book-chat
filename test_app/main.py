# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from backend.context import get_context, index_data

load_dotenv()
app = FastAPI()

index_data("books")

api_base = os.getenv("OPENAI_API_BASE_URL")  
api_key = os.getenv("OPENAI_API_KEY")
api_model = os.getenv("OPENAI_API_MODEL")

client = OpenAI(
    base_url= api_base, # "http://<Your api-server IP>:port"
    api_key = api_key
)


# Para que React pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir a "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("app ready!!")

class Query(BaseModel):
    query: str

@app.post("/recommend")
def recommend(query: Query):
    # Simulación de respuesta desde RAG o CSV
    search_result = get_context(query.query)
    chat_bot_response = assistant(query.query, search_result)
    return {'response': chat_bot_response}

def assistant(query, context):
    messages=[
        # Set the system characteristics for this chat bot
        {"role": "system", "content": "Assistant is a chatbot that helps you find a good book recommendation."},
        # Set the query so that the chatbot can respond to it
        {"role": "user", "content": query},
        # Add the context from the vector search results so that the chatbot can use
        # it as part of the response for an augmented context
        {"role": "Assistant", "content": str(context)}
    ]

    response = client.chat.completions.create(
        model = api_model,
        messages=messages,
    )
    return response.choices[0].message