# book-chat
This end-to-end chatbot application recommends books based on user queries using a RAG (Retrieval-Augmented Generation) approach. Starting with a Kaggle dataset, I enriched the data via web scraping from OpenLibrary and Google Books to ensure completeness. The dataset was cleaned, filtered with SQL, and indexed using Azure Cognitive Search.


Embeddings were generated with OpenAI's text-embedding-ada-002 model, and responses were powered by gpt-4.1. The frontend was built with React and JavaScript, and the entire app was deployed to Azure Container Apps. Logs are monitored in real time via the terminal, supporting full observability and debugging.

The app was deployed in azure container apps using free subscription plan. Therefore 2 apps are available in this repo.

### Local app
In test_app the application can be executed using a llama file local model.

The app can be used creating an image in Docker using the same DockerFile as in app folder.

### Azure app
Currently unavailable but recordings of its use and logs monitoring are shown in this file. 

