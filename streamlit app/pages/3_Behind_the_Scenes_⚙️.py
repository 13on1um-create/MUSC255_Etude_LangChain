import streamlit as st


st.set_page_config(page_title='Behind the Scenes', page_icon='⚙️')

st.sidebar.header('Behind the Scenes ⚙️')

st.title('Operations & Moving Parts ⚙️')

st.markdown(
    """
    ### The Archive
    A publically accessible archive of all _The Etude_ magazines 
    [exists](https://digitalcommons.gardner-webb.edu/etude/) and is graciouslly 
    provided by Digital Commons @ Gardner-Webb University, which is where this 
    project is pulling its files from. These files are provided in partially 
    searchable PDF format.
    ### The LLM
    OpenAI's gpt-5-mini multimodal LLM model powers the operations behind this
    project. 
    ##### Processing PDFs
    The OCR (Optical Character Recognition, aka text extraction from an
    image) done on the archives is only partial and rather poor; _The Etude_ is a
    magazine, which is extremely difficult to OCR due to its
    winding structures and heavily stylized presentation. The PDFs used
    for the sample dataset in this project were further processed using OpenAI
    Vision to much more accurately extract text from and describe images within the
    magazines. The source code and processed text files are available 
    [on GitHub]().
    ##### Answering Queries
    RAG (Retrieval-Augmented Generation) assists gpt-5-mini in calculating its
    response by pointing it towards roughly relevant chunks of text within the
    dataset so gpt-5-mini has only a small part of the dataset to analyze instead
    of the whole shebang. More on RAG below.
    
    gpt-5-mini processes the text chunks passed by RAG to determine its answer
    to your query. These text chunks are passed as _context_. It is instructed 
    via command prompt not to relay any information not found in the passed
    context as a safeguard against hallucinations. It will defer to answering
    "I don't know", as instructed, if it has low confidence in whether its answer
    passes that command prompt.
    ### The RAG
    Chroma, the open-source vector database, is used to power our RAG implementation.
    ##### Chunking
    Our processed text documents are carved up into smaller chunks using Chroma's
    recursive text splitter object, which tries to create chunks of a certain size
    (ours is 2000 characters) with a certain amount of overlap to preserve context
    (ours is 300 characters) while prioritizing splitting chunks by paragraph,
    then sentence, then word. 
    For English documents, the recommended chunk and overlap size are about
    1000-2000 and 200-400 characters respectively. The chunk size for this project
    was chosen assuming that a small number of chunks would be fetched for each
    LLM query. For more discussion on chunk size, see [this article](https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5).

    Because our processed documents extracted text exactly in the order a human would
    read them (left to right columns, top to bottom), we don't need to worry about
    columns while chunking; the proper ordering was already determined.
    ##### Embedding
    Chroma _embeds_ each text chunk with an extremely high-dimensional vector that
    relates them all within a similarity space, essentially plotting each vector
    into the extremely high-dimensional space according to how closely related
    they are based on the language within them. These embeddings are then saved into
    a vector database. This project currently uses a database of 3022 chunks (78.2 MB).
    
    When the user issues a query, that query is also embedded with a vector, and
    Chroma passes the most relevant text chunks to the LLM based on the position
    of that vector within the similarity space compared to the position of the text
    chunks.
    ### 
"""
)