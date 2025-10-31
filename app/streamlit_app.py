import streamlit as st
import pandas as pd
from io import StringIO
import base64
from functions import *


st.write("""
# LLM RAG PDF Extractor
Hello *Everyone!!*
""")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)
#
with col1:
    text_input = st.text_input(
        "Enter your OPENAI key here!",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
    uploaded_file = st.file_uploader("Choose a document")

    # Load in the documents
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)
        #
        # # To read file as string:
        # string_data = stringio.read()
        # st.write(string_data)
        #
        # # Can be used wherever a "file-like" object is accepted:
        # dataframe = pd.read_csv(uploaded_file)
        # st.write(dataframe)

    else:
        uploaded_file = ""

    with st.form("my_form"):
        api_key_val = text_input
        pdf_val = uploaded_file

        submitted = st.form_submit_button(label="EXTRACT")
        if submitted:
            print(api_key_val)
           # print(pdf_val)
            pass

with col2:
    if uploaded_file:

        st.pdf(uploaded_file, height="stretch", key=None)
    else:
        st.text("")