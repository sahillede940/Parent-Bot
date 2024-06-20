import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MODEL_ENDPOINT = os.environ["MODEL_ENDPOINT"] # Model endpoint
    PHI3_API_KEY = os.environ["PHI3_API_KEY"] # API key
    TEXT_EMBEDDING_DEPLOYMENT_NAME = os.environ["TEXT_EMBEDDING_DEPLOYMENT_NAME"] # Text embedding deployment name
    AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"] # OpenAI API key
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"] # OpenAI endpoint
    SECRET_AZURE_SEARCH_KEY = os.environ["SECRET_AZURE_SEARCH_KEY"] # Azure search key
    AZURE_SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"] # Azure search endpoint
    INDEX_NAME = os.environ["INDEX_NAME"] # Index name