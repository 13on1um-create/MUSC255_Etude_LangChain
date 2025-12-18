import streamlit as st


st.set_page_config(page_title='Acknowledgements', page_icon='🙏')

st.sidebar.header('Acknowledgements 🙏')

st.title('Acknowledgements & Citations 🙏')

st.markdown(
    """
    ### Annotated Bibliography
    Chroma. 2025. "Chroma Docs". Accessed November 5, 2025. [https://docs.trychroma.com/docs](https://docs.trychroma.com/docs).

    > Chroma documentation; consulted throughout this project.

    Cross, Charlie. 2025. "RAG: Haverford College Concert Programs Fall 2009 - Spring 2022". Published June 26, 2025. [https://cwcross.github.io/Encoding-Music-Summer-2025/HC%20All%20Programs/full_concert_programs.html](https://cwcross.github.io/Encoding-Music-Summer-2025/HC%20All%20Programs/full_concert_programs.html).
    
    > One of Charlie Cross's notebooks demonstrating a RAG implementation with LLM, which I used as a base from which to learn the ropes of LLM and RAG deployment.

    Dennis, Pam. _The Etude Magazine: 1883-1957_. Digital Commons @ Gardner-Webb University, Boiling Springs, North Carolina. https://digitalcommons.gardner-webb.edu/etude/.

    > The archive of _The Etude_ magazine PDFs accessed for this project.

    Heimann, William Keith. "'This Is War!': Musical Images Used as Propaganda in _The Etude Music Magazine_." _Music in Art_ 41, no. 1-2 (2016): 141-61. https://www.jstor.org/stable/90012993.

    > Information from this article was used to inform the synopsis of _The Etude_ on the home page of this app. It may be used further to inform later expansions of functionality.

    LangChain Docs. 2025. "Docs by LangChain". Accessed November 5, 2025. [https://docs.langchain.com](https://docs.langchain.com).
    
    > LangChain documentation; consulted throughout this project.

    OpenAI Python API library. "openai/openai-python". GitHub. Accessed December 16, 2025. [https://github.com/openai/openai-python](https://github.com/openai/openai-python).

    > Contains examples and tutorial documentation. Consulted particularly during the OCR portion of this project.

    Theja, Ravi. "Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex". LlamaIndex. Published October 5, 2023. https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5.

    > Consulted the results of this article to inform my choice of chunk size and also to educate myself on chunking in general.

    ### Acknowledgements
    Thank you to Charlie Cross and Daniel Russo-Batterham sharing their expertise and 
    consulting with me about this project. They were a huge help.

    Thank you again to them, but especially to Professor Freedman, for making MUSC255
    this semester such an intellectually stimulating and curious adventure for me.
    I will forever aspire to be as hyped as Professor Freedman is about the things
    that I'm passionate about. In the spirit of the intrepidity that he espouses, I
    will probably continue expanding this project (with my own money this time) out of
    simple interest for where it could go.

    I'll see you all after break.

    ♥♥
"""
)