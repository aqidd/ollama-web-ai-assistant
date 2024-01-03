import logging
import os
import sys
from typing import Any, Dict, Generator, List, Union

import streamlit as st
from llama_index import ServiceContext, StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama_embedding import OllamaEmbedding

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

ResponseType = Union[Generator[Any, None, None], Any, List, Dict]

service_context = ServiceContext.from_defaults(llm=Ollama(model="mistral", request_timeout=1000 * 60 * 60), embed_model=OllamaEmbedding(model_name="mistral"))

@st.cache_resource(show_spinner=False)  # type: ignore[misc]
def load_index() -> Any:
    """Load the index from the storage directory."""
    print("Loading index...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, ".kb")

    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=dir_path)
    # load index
    index = load_index_from_storage(storage_context, service_context=service_context)
    query_engine = index.as_query_engine()
    print("Done.")
    return query_engine


def main() -> None:
    """Run the chatbot."""

    if "query_engine" not in st.session_state:
        st.session_state.query_engine = load_index()
        
    st.title("Chat with BlogAI Assistant!!")
    st.write("All about <YOUR_WEBSITE>. Ask away your questions!")

    if "messages" not in st.session_state:
        system_prompt = (
            "Your purpose is to answer questions about specific documents only. "
            "Please answer the user's questions based on what you know about the document. "
            "If the question is outside scope of the document, please politely decline. "
            "If you don't know the answer, say `I don't know`. "
        )
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    for message in st.session_state.messages:
        if message["role"] not in ["user", "assistant"]:
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            print("Querying query engine API...")
            response = st.session_state.query_engine.query(prompt)
            full_response = f"{response}"
            print(full_response)
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
