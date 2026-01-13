from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding



DOCUMENT_PATH = "docs/extensions"
STORAGE_PATH = "storage"
splitter = SentenceSplitter( chunk_size=400, chunk_overlap=8 )

documents = SimpleDirectoryReader(DOCUMENT_PATH).load_data()

nodes = splitter.get_nodes_from_documents(documents)

storage_context = StorageContext.from_defaults()

index = VectorStoreIndex(nodes, embed_model=OllamaEmbedding(model_name="nomic-embed-text", base_url="http://localhost:11434"), storage_context=storage_context)

storage_context.persist(persist_dir=STORAGE_PATH)

print("Index built and stored in", STORAGE_PATH)
