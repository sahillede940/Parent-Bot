import PyPDF2.errors
from config import Config
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    ComplexField,
    CorsOptions,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration
)
import asyncio
from langchain_openai import AzureOpenAIEmbeddings
from PyPDF2 import PdfReader
import PyPDF2
import os

def get_doc_data(embeddings):
    path_to_data = '../data/'
    files = os.listdir(path_to_data)
    data = []
    for i in range(len(files)):
        try:
            data1 = PdfReader(f"{path_to_data}{files[i]}", strict=False)
            txt = ''
            for page in data1.pages:
                txt += page.extract_text()
            print(f"Embedding {files[i]}")
            doc = {
                "docId": f"{i + 1}",
                "docTitle": files[i],
                "description": txt,
                "descriptionVector": embeddings.embed_query(txt)
            }
            data.append(doc)
        except PyPDF2.errors.PdfReadError:
            print(f"Error reading {files[i]}")
            continue   
    return data


async def create_index_if_not_exists(client: SearchIndexClient, name: str):
    doc_index = SearchIndex(
        name=name,
        fields=[
            SimpleField(
                name="docId", type=SearchFieldDataType.String, key=True),
            SimpleField(name="docTitle", type=SearchFieldDataType.String),
            SearchableField(name="description",
                            type=SearchFieldDataType.String, searchable=True),
            SearchField(name="descriptionVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=1536, vector_search_profile_name='my-vector-config'),
        ],
        scoring_profiles=[],
        cors_options=CorsOptions(allowed_origins=["*"]),
        vector_search=VectorSearch(
            profiles=[VectorSearchProfile(
                name="my-vector-config", algorithm_configuration_name="my-algorithms-config")],
            algorithms=[HnswAlgorithmConfiguration(
                name="my-algorithms-config")],
        )
    )

    client.create_or_update_index(doc_index)


async def setup(search_api_key, search_api_endpoint):
    index = 'data'

    credentials = AzureKeyCredential(search_api_key)

    search_index_client = SearchIndexClient(search_api_endpoint, credentials)
    await create_index_if_not_exists(search_index_client, index)
    
    print("Create index succeeded. If it does not exist, wait for 5 seconds...")
    await asyncio.sleep(5)

    search_client = SearchClient(search_api_endpoint, index, credentials)

    embeddings = AzureOpenAIEmbeddings(
        api_key=Config.AZURE_OPENAI_API_KEY,
        model=Config.TEXT_EMBEDDING_DEPLOYMENT_NAME,
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
    )
    data = get_doc_data(embeddings=embeddings)
    search_client.merge_or_upload_documents(documents=data)

    print("Upload new documents succeeded. If they do not exist, wait for several seconds...")
    
search_api_key = Config.SECRET_AZURE_SEARCH_KEY
search_api_endpoint = Config.AZURE_SEARCH_ENDPOINT
asyncio.run(setup(search_api_key, search_api_endpoint))
print("setup finished")
