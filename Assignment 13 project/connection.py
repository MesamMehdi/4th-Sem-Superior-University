import weaviate
from weaviate.classes.init import Auth
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
cluster_url = os.getenv("WEAVIATE_URL")
weaviate_api = os.getenv("WEAVIATE_API_KEY")
LLM = os.getenv("MODEL_NAME")
vectorizer = os.getenv("VECTORIZER")
huggingface_api = os.getenv("HUGGINGFACE_APIKEY")
base_url = os.getenv("BASE_URL")
openrouter_apikey = os.getenv("OPENROUTER_APIKEY")
print("Environment Variables loaded..")


def connectDB():
    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=cluster_url,
            auth_credentials=Auth.api_key(weaviate_api),
            headers={"X-HuggingFace-Api-Key": huggingface_api},
        )
        if not client.is_ready():
            raise ConnectionError("Connection Failed..")

        print("Successfully Connected to Weaviate Cloud..")
        return client
    except Exception as e:
        print(e)


def LLM_Connect(prompt):
    try:
        client = OpenAI(base_url=base_url, api_key=openrouter_apikey)
        response = client.chat.completions.create(
            model=LLM,
            messages=[
                {"role": "system", "content": "You are a recommendation bot"},
                {"role": "user", "content": prompt},
            ],
            timeout=10,
        )
        print("LLM Connnected..")
        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return "Sorry, I'm having trouble generating recommendations right now."


# prompt = "Hi how are you?"
# client = connectDB()
# response = LLM_Connect(prompt)
# print(response)
# client.close()
