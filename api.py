from quart import Quart, request, jsonify
from query_index import search_query_agent

app = Quart(__name__)

@app.route('/api/v1/chat', methods=['POST'])
async def chat():
    data = await request.get_json()
    query = data.get('query')
    response = await search_query_agent(query)
    return jsonify({'query': query, 'response': response})

if __name__ == '__main__':
    app.run(debug=True)