from flask import Flask, request, jsonify
from QnA.model import phi3
# imstall cors
from flask_cors import CORS


app = Flask(__name__)
path_to_data = '../data/'
CORS(app)

# flask --app app.py --debug run
@app.route('/api/message', methods=['POST'])
def get_message():
    if request.method == 'POST':
        # get last message from user
        message = request.json.get('messages')
        query = message[-1].get('content')[0].get('text')
        if query:
            response = phi3(query)
            response = response.get("choices")[0].get("message").get("content")
            with open('response.txt', 'w') as f:
                f.write(response)
            return jsonify({"text": response})
        else:
            return jsonify({"error": "No query provided"})


if __name__ == '__main__':
    app.run(debug=True, port=8000)