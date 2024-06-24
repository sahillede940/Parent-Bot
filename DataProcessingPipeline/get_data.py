from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

def get_pdfs():
    loader = DirectoryLoader(
        path="./data2",
        show_progress=True,
        loader_cls=PyPDFLoader,
        glob="*",
        use_multithreading=True,
    )
    docs = loader.load()
    return docs