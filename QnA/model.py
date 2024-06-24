import json
import os
import ssl
import requests
from config import Config
import pprint
from .promt_template import PROMPT, system_prompt
from .similarity_search import similarity_search


def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


def format_message(question, context):
    return [
        {
            'role': 'user',
            'content': system_prompt
        }, {
            'role': 'user',
            'content': PROMPT.format(context=context, question=question)
        }
    ]


def phi3(query, max_tokens=1024, temperature=0.7, top_p=1):
    allowSelfSignedHttps(True)

    messages = format_message(query, context=similarity_search(query))

    data = {
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }

    url = Config.MODEL_ENDPOINT
    api_key = Config.PHI3_API_KEY

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        with open("data.json", "w") as f:
            json.dump(data, f)
        body = json.dumps(data)
        req = requests.post(url, headers=headers, data=body)
        response = req.json()

        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""