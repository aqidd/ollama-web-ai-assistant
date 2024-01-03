import logging
import os
import sys
from shutil import rmtree

from llama_index import ServiceContext, SimpleDirectoryReader, TreeIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama_embedding import OllamaEmbedding

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

service_context = ServiceContext.from_defaults(llm=Ollama(model="mistral", request_timeout=1000 * 60 * 60), embed_model=OllamaEmbedding(model_name="mistral"))

def build_index(data_dir: str, knowledge_base_dir: str) -> None:
    """Build the vector index from the markdown files in the directory."""
    print("Building vector index...")
    documents = SimpleDirectoryReader(data_dir).load_data()

    index = TreeIndex.from_documents(documents, service_context=service_context)
    index.storage_context.persist(persist_dir=knowledge_base_dir)
    print("Done.")
    

def main() -> None:
    """Build the vector index from the markdown files in the directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_base_dir = os.path.join(base_dir, ".kb")
    # Delete Storage Directory
    if os.path.exists(knowledge_base_dir):
        rmtree(knowledge_base_dir)
    data_dir = os.path.join(base_dir, "content", "blogs")
    build_index(data_dir, knowledge_base_dir)


if __name__ == "__main__":
    main()
