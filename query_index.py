from llama_index.core import StorageContext, load_index_from_storage, Settings, ServiceContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.agent.workflow import FunctionAgent
import uvloop

llm = Ollama(model="qwen2.5:0.5b", base_url="http://localhost:11434", request_timeout=120.0)

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url="http://localhost:11434")

STORAGE_PATH = "storage"

storage_context = StorageContext.from_defaults(persist_dir=STORAGE_PATH)
index = load_index_from_storage(storage_context=storage_context)

query_engine = index.as_query_engine(similarity_top_k=5, llm=llm)
response = query_engine.query("author gave thanks to whoom?")
print(str(response))
# return;

async def search_query(query: str) -> str:
    query_engine = index.as_query_engine(similarity_top_k=5, llm=llm)
    response = await query_engine.aquery(query)
    return str(response)

agent = FunctionAgent(
    tools=[search_query], 
    llm=llm, 
    system_prompt="you are a helpful assistant that can answer questions through the documents in the storage."
)

async def main():
    response = await agent.run("author gave thanks to whoom?")
    print(str(response))

# if __name__ == "__main__":
    # uvloop.run(main())