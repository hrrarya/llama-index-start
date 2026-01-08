from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

llm = Ollama(
    model="qwen2.5:3b",  # Embedding-optimized model
    base_url="http://localhost:11434",
    request_timeout=120.0
)
# Settings.llm = None

splitter = SentenceSplitter( chunk_size=200, chunk_overlap=4 )  

documents = SimpleDirectoryReader( 'docs/dummy' ).load_data()

nodes = splitter.get_nodes_from_documents(documents)

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",  # Embedding-optimized model
    base_url="http://localhost:11434"
)
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)

query_engine = index.as_query_engine(
    llm=llm
)

response = query_engine.query("can i show popup based on user roles using popup pro?")
print(str(response))

