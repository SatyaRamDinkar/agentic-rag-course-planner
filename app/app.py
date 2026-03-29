import streamlit as st
from src.rag_pipeline import ask_question

st.title("🎓 Course Planning Assistant")

query = st.text_input("Ask your question")

if st.button("Submit"):
if query:
response = ask_question(query)
st.write(response)


