import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Wiki Summary", page_icon="📚")
st.title("📚 Wiki Summary Demo")
st.write("Enter a query below to fetch and summarize a Wikipedia article.")

# Input field for the user's query\query = st.text_input("Your query:", placeholder="e.g., history of Agentic AI")
query = st.text_input("Your query:", placeholder="e.g., history of Agentic AI")
if st.button("Summarize"):
    if not query.strip():
        st.warning("Please enter a search query before summarizing.")
    else:
        with st.spinner("Fetching and summarizing…"):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/summarize",
                    json={"query": query},
                    timeout=60
                )
                resp.raise_for_status()
                data = resp.json()

                st.subheader(data.get("title", "Summary"))
                st.write(data["summary"])
                st.markdown(f"**Source:** [{data['source_url']}]({data['source_url']})")

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching summary: {e}")
