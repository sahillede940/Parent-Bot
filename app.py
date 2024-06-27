from flask import Flask, request, jsonify
from QnA.model import phi3
from flask_cors import cross_origin

from flask_cors import CORS
from config import Config


app = Flask(__name__)
path_to_data = '../data/'
# make publically available
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


# flask --app app.py --debug run


@app.route('/api/message', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_message():
    if request.method == 'POST':
        # get last message from user
        message = request.json.get('messages')
        if message:
            response = phi3(message)
            return jsonify({"text": response})
        else:
            return jsonify({"error": "No query provided"})


@app.route('/api/test', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def test():
    return jsonify({"text": "Hello World!"})


"""
    Was tryping to use local embeddings model
"""
