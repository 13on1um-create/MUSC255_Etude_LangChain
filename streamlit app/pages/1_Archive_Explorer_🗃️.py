import streamlit as st
import requests
from streamlit_pdf_viewer import pdf_viewer


st.set_page_config(page_title='Archive Explorer', page_icon='🗃️')

st.sidebar.header('Archive Explorer 🗃️')
st.title('Archive Explorer 🗃️')
st.markdown(
    """
    Use this page as a navigator for the Etude archives as provided by Digital Commons @ Gardner-Webb University. More functionality may be added later.
"""
)

i = st.slider(label="Archive ID (unfortunately not chronologically ordered)", min_value=1001, max_value=1882)

if st.checkbox('Load PDF'):
    response = requests.get(
        f'https://digitalcommons.gardner-webb.edu/cgi/viewcontent.cgi?article={i}&context=etude'
    )
    pdf_viewer(response.content,
            width=700,
            height=1000,
            viewer_align='center',
            show_page_separator=True)