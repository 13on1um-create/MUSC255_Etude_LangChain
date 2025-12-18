import streamlit as st


st.set_page_config(page_title='Home', page_icon='🏠')

st.title("Exploring _The Etude_ Using LLM 🔍")

st.markdown(
    """
    _The Etude_, published by Theodore Presser Company between 1883 and 1957, was a
    music magazine aimed at musicians of all levels throughout the country, becoming
    a staple for American music teachers in particular. Began mainly as a pedagogical
    and educational consult for piano teachers and students, it eventually grew to also 
    print articles about other instruments, voice, and less-involved musical items 
    that you might call the "popular music" of its time. Its 70+ years of consistent
    publication divulge insight into the development of not only music and music education 
    in the U.S., but also of the culture surrounding American music practice and American
    music publishing at large. 
    
    Access to these magazines is provided by
    [Digital Commons @ Gardner-Webb University](https://digitalcommons.gardner-webb.edu/etude/).

    ### The Main Project
    This project provides an interface that liaises between an LLM and a sample of 
    about 20 processed issues of _The Etude_. Using RAG (Retrieval-Augmented Generation),
    the interface is tailored to answer needle-in-a-haystack style queries of the sample
    dataset, although more functionality and more data may be added later. To try out the 
    interface, **👈 select "LLM RAG" from the sidebar**. 

    ### Ancillary Materials
    An in-house viewer of the Digital Commons @ Gardner-Webb University archive is
    also available for convenience. **👈 select "Archive Explorer" from the sidebar**
    to use it.
    
    **👈 Select "Behind the Scenes" from the sidebar** for more information about
    the operations of this project.
"""
)