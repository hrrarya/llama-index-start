from quart import Quart, request
import json
import sys
from pathlib import Path

# Add parent directory to path to import query_index
sys.path.insert(0, str(Path(__file__).parent.parent))

from query_index import search_query

app = Quart(__name__)

@app.get("/say-hello")
def index():
    return json.dumps({"message": "Hello, World!"})

@app.post("/say-my-name")
async def say_my_name():
    data = await request.get_json()
    name = data.get("name")
    return json.dumps({"message": f"Hello, {name}!"})



@app.post("/ask-question")
async def ask_question():
    data = await request.get_json()
    question = data.get("question")
    response = await search_query(question)
    return json.dumps({"message": str(response)})

if __name__ == "__main__":
    app.run(debug=True)