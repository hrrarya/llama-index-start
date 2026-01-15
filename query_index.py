from llama_index.core import StorageContext, load_index_from_storage, Settings, ChatPromptTemplate
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.core.agent.workflow import FunctionAgent
import uvloop

llm = Ollama(model="gemma3:4b", base_url="http://localhost:11434", request_timeout=120.0)
# llm = Ollama(model="qwen2.5:0.5b", base_url="http://localhost:11434", request_timeout=120.0)

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url="http://localhost:11434")

STORAGE_PATH = "storage"

storage_context = StorageContext.from_defaults(persist_dir=STORAGE_PATH)
index = load_index_from_storage(storage_context=storage_context)

qa_prompt_str = (
    "You are an expert support assistant for My Products.\n"
    "Follow these rules strictly:\n"
    "1. Only use the provided context.\n"
    "2. If the answer is not in the context, say 'I don’t have relevant context in the documentation to answer that accurately'.\n"
    "3. Answer in concise Markdown.\n\n"
    "Context:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "User question: {query_str}\n"
)

text_qa_template = ChatPromptTemplate.from_messages(
    [
        ("system", qa_prompt_str),
    ]
)

async def search_query(query: str) -> str:
    query_engine = index.as_query_engine(similarity_top_k=5, llm=llm, text_qa_template=text_qa_template)
    response = await query_engine.aquery(query)
    return response


async def main():
    # agent = FunctionAgent(
    #     tools=[search_query], 
    #     llm=llm, 
    #     system_prompt="you are a helpful assistant that can answer questions through the documents in the storage."
    # )
    # response = await agent.run(user_msg="how can i add a new popup?")
    # response = await search_query("how can i enable popup pro in divi builder accordion to documents?")
    # response = await search_query("tell me about donald trump")
    response = await search_query("How can the language dropdown be removed from the header top? I just need a clear, non-destructive explanation.")
    print(str(response))

if __name__ == "__main__":
    uvloop.run(main())