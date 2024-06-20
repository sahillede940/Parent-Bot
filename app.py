from flask import Flask, request, jsonify
from model import phi3

app = Flask(__name__)
path_to_data = '../data/'


@app.route('/api/message', methods=['POST'])
def get_message():
    if request.method == 'POST':
        messages = request.json.get('messages')
        response = phi3(
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1
        )
        return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
