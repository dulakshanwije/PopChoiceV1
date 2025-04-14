from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from movies.search_movie import search_movie

app = Flask(__name__)

CORS(app, resources={
    r"/*": {"origins": ["http://localhost:5173"]}
},headers='Content-Type')

@app.route('/suggest/', methods=['POST'])
def chat():
    content = request.get_json()
    
    if not content:
        return make_response(jsonify({
            'success':False,
            'error': "Invalid request."
        }))
    if "content" not in content:
        return make_response(jsonify({
            'success':False,
            'error': "Content parameter is missing."
        }))

    reply = search_movie(content['content'])
    
    if reply["success"] == False:
        return make_response(jsonify({
            'success':False,
            'error': reply["error"]
        }))
    
    return make_response(jsonify({
        'success':True,
        'content':reply
    }))

if __name__ == "__main__":
    app.run(debug=True)