import glob
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


"""
ONLY RUN THIS FILE ONCE.
"""

os.environ["OPENAI_API_KEY"] = 'openai-api-key-here'

embeddings = OpenAIEmbeddings(model='text-embedding-3-large')

vector_store = Chroma(
    collection_name="Etude_samples",
    embedding_function=embeddings,
    persist_directory='./chroma-db'
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=300,
    length_function=len,
    is_separator_regex=False
)

for processed_document in glob.glob('processed-documents/*'):
    with open(processed_document, 'r', encoding='utf-8') as f:
        text = f.read()
        chunks = text_splitter.create_documents([text])
        vector_store.add_documents(documents=chunks)
        print(f'Created {len(chunks)} chunks from {processed_document}')

print('chroma-db complete')