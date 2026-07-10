import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="PDF Q&A Assistant", page_icon="📄", layout="wide")
st.title("PDF Upload and Retrieval Chat")

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "active_doc_id" not in st.session_state:
    st.session_state.active_doc_id = None

with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if st.button("Upload and process", use_container_width=True, disabled=uploaded_file is None):
        if uploaded_file is None:
            st.warning("Please select a PDF file before uploading.")
        else:
            with st.spinner("Uploading and processing the document..."):
                try:
                    files = {
                        "document": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    }
                    response = requests.post(
                        f"{BACKEND_URL}/pdf_post",
                        files=files,
                        timeout=300,
                    )
                    response.raise_for_status()
                    data = response.json()
                    doc_id = data.get("doc_id")

                    if doc_id:
                        st.session_state.chat_sessions[doc_id] = {
                            "filename": uploaded_file.name,
                            "messages": [
                                {
                                    "role": "assistant",
                                    "content": (
                                        "Document uploaded successfully. "
                                        f"Doc ID: {doc_id}. "
                                        "You can now ask questions about it."
                                    ),
                                }
                            ],
                        }
                        st.session_state.active_doc_id = doc_id
                        st.success("Document uploaded successfully")
                    else:
                        st.error("The upload did not return a document ID.")
                except requests.RequestException as exc:
                    st.error(f"Upload failed: {exc}")

    if st.session_state.chat_sessions:
        session_ids = list(st.session_state.chat_sessions.keys())
        if st.session_state.active_doc_id not in session_ids:
            st.session_state.active_doc_id = session_ids[0]

        selected_doc_id = st.selectbox(
            "Chat sessions",
            options=session_ids,
            index=session_ids.index(st.session_state.active_doc_id),
            format_func=lambda doc_id: (
                f"{st.session_state.chat_sessions[doc_id]['filename']} ({doc_id})"
            ),
        )
        if selected_doc_id != st.session_state.active_doc_id:
            st.session_state.active_doc_id = selected_doc_id

        st.caption(f"Active document ID: {st.session_state.active_doc_id}")

if not st.session_state.chat_sessions or not st.session_state.active_doc_id:
    st.info("Upload a PDF from the sidebar to start a chat session.")
    st.stop()

current_session = st.session_state.chat_sessions[st.session_state.active_doc_id]
st.subheader(f"Current topic: {current_session['filename']}")

for message in current_session["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about the uploaded document")

if prompt:
    current_session["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving answer..."):
            try:
                payload = {
                    "doc_id": st.session_state.active_doc_id,
                    "query": prompt,
                }
                response = requests.post(
                    f"{BACKEND_URL}/retriver_get",
                    json=payload,
                    timeout=300,
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get("message") or "No response was returned."
            except requests.RequestException as exc:
                answer = f"Retrieval failed: {exc}"

        st.markdown(answer)

    current_session["messages"].append({"role": "assistant", "content": answer})
