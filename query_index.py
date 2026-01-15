from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.agent.workflow import FunctionAgent
import uvloop

llm = Ollama(model="phi4-mini:3.8b", base_url="http://localhost:11434", request_timeout=120.0)
Settings.llm = llm
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url="http://localhost:11434")

STORAGE_PATH = "storage"

storage_context = StorageContext.from_defaults(persist_dir=STORAGE_PATH)
index = load_index_from_storage(storage_context=storage_context)

async def search_query(query: str) -> str:
    """
    Search the documentation index for relevant information about the given query.
    Use this tool to find information about documentation, features, or topics.
    
    Args:
        query: The search query string
        
    Returns:
        str: Relevant documentation content matching the query
    """
    query_engine = index.as_query_engine(similarity_top_k=3, response_mode="tree_summarize")
    response = await query_engine.aquery(query)
    # print(response)
    return str(response)

agent = FunctionAgent(
    tools=[search_query], 
    llm=llm,  
    system_prompt = """
You MUST call the search_query tool before answering any question.
You MUST answer using ONLY the returned document text from the tool.
If the tool returns no relevant information, reply exactly with:
"I don't know based on the provided documentation."
Do NOT use prior knowledge.
""",
    # allow_parallel_tool_calls=False,
)


async def search_query_agent(query: str) -> str:
    response = await agent.run(query)
    return str(response)

async def main():
    response = await agent.run("what is popup pro?")
    # response = await search_query_agent("how to add a new popup pro")
    print(str(response))

if __name__ == "__main__":
    uvloop.run(main())