from connection import connectDB, LLM_Connect
import streamlit as st
import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth
import weaviate.classes.config as wc
import weaviate.classes as wvc
from openai import OpenAI
import os


load_dotenv()
weaviate_apikey = os.getenv("WEAVIATE_API_KEY")
cluster_url = os.getenv("WEAVIATE_URL")
openrouter_apikey = os.getenv("OPENROUTER_APIKEY")
huggingface_apikey = os.getenv("HUGGINGFACE_APIKEY")
model = os.getenv("MODEL_NAME")
vectorizer = os.getenv("VECTORIZER")
base_url = os.getenv("BASE_URL")

client = connectDB()
books = client.collections.get("Book_Data")

st.set_page_config(page_title="Book Recommender", layout="centered")
st.title("📚 Book Recommendation Bot")

st.markdown("Ask me for book suggestions based on a genre, author, or book title!")

user_query = st.text_input(
    "Enter your query:", placeholder="What type of book do you want?"
)


def recommend_books(query):
    result = books.query.hybrid(
        query=query,
        query_properties=["title", "author", "language", "description"],
        limit=5,
    )

    context = ""
    for obj in result.objects:
        properties = obj.properties
        context += f"""
### Title:
{properties.get('title', 'N/A')}

### Author:
{properties.get('author', 'N/A')}

### Rating:
{properties.get('rating', 'N/A')}

### Language:
{properties.get('language', 'N/A')}

### Description:
{properties.get('description', 'N/A')}

"""

    final_prompt = f"""You are a helpful and knowledgeable book recommendation assistant.

User query: "{query}"

Here are some related books retrieved from the database:

{context}

Based on this information, recommend 2-3 of the most relevant books. Use the following format for each:

### Title:
[Book Title]

### Author:
[Author Name]

### Rating:
[Rating out of 5]

### Language:
[Language]

### Description:
[Concise and engaging description]

Only recommend books relevant to the user's query. Respond in this structured format."""

    response = LLM_Connect(final_prompt)
    return response


if user_query:
    st.markdown("### Recommended Books:")
    recommendation = recommend_books(user_query)
    st.write(recommendation)
    client.close()