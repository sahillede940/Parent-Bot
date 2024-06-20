import json
import os
import ssl
import requests
from config import Config
import pprint



def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


def format_message(messages, context):
    query = messages[-1]['content']
    # remove the last message from the list
    messages = messages[:-1]
    query = f"<context>{context}</context>\n\n Query: {query}"
    with open('Prompt/skprompt.txt', 'r') as file:
        prompt = file.read()
    prompt = [{
            "role": "system",
            "content": prompt
        }]
    user_prompt = {
        "role": "user",
        "content": query
    }
    messages = messages[-3:]
    prompt.extend(messages)
    prompt.append(user_prompt)
    return prompt

def phi3(messages, max_tokens=1024, temperature=0.7, top_p=1):
    allowSelfSignedHttps(True)

    messages = format_message(messages, context="How to train a model in Python?")
    pprint.PrettyPrinter(indent=2).pprint(messages)

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
        body = json.dumps(data)
        req = requests.post(url, headers=headers, data=body)
        response = req.json()

        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
