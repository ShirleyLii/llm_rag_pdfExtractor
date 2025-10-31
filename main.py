import streamlit as st
from functions import *

st.write("""
# LLM RAG PDF Extractor
Hello *Everyone!!*
""")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False


text_input = st.text_input(
    "Enter your OPENAI key here!",
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
)
uploaded_file = st.file_uploader("Choose a document")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    text = bytes_data.decode('utf-8', errors='ignore')  # skip invalid chars
    doc = list(text)
    with st.expander("PDF File preview"):
        st.pdf(uploaded_file, height="stretch", key=None)

with st.form("my_form"):
    api_key_val = text_input
    pdf_val = uploaded_file

    submitted = st.form_submit_button(label="EXTRACT")
    if submitted and uploaded_file is not None:
        with st.spinner("⚙️ Processing your document... This may take a few seconds."):
            try:

                print(api_key_val)
                embedding = get_embedding_function(api_key_val)
                vectorstore = load_vectorstore(text, embedding, 'test')
                llm = connect_chat_openai(api_key_val)
                prompt = prompt(vectorstore, llm)

            except Exception as error:
                st.error(" Error Occurred. Please check with admin with the logs.")
            else:
                st.success("✅ Done!")
                st.dataframe(prompt)

    elif submitted and uploaded_file is None:
        st.error("You have no upload any document for extraction yet :)")
