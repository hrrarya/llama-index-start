# from langchain_text_splitters import CharacterTextSplitter
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex
# import os
# os.environ["OPENAI_API_KEY"] = ""

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

# Settings.llm = None

splitter = SentenceSplitter( chunk_size = 200, chunk_overlap = 4 )

documents = SimpleDirectoryReader( 'docs/dummy' ).load_data()
# text = documents[0].text

nodes = splitter.get_nodes_from_documents( documents )

embed_model = Ollama(model="qwen2.5:3b", base_url="http://localhost:11434")

index = VectorStoreIndex(
    nodes,
    embed_model=embed_model,
)
# response = embed_model
# print(index)

query_engine = index.as_query_engine(
    similarity_top_k=5,
    # llm=None,
)

response = query_engine.query("How to enable Popup Pro in divi?")
print(response)