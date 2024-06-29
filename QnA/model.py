from .similarity_search import similarity_search
from .promt_template import info_context, system_prompt, user_prompt
from config import Config
import json
import os
import ssl
import requests
import sys
sys.path.append("..")


def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


ROLE = "user" if Config.PHI3_LOCATION == "azure" else "system"
print(ROLE)


def format_message(message):

    # get the last 2 messages from the user and last 2 message of the assistant
    req_message = []
    req_message.append({
        "role": ROLE,
        "content": system_prompt.format(
            guardian_name=Config.GUARDIAN_NAME,
            children_name=Config.STUDENT_NAME,
            school_name=Config.SCHOOL_NAME
        )
    })

    max_conversation_to_feed = 2
    prev = -(max_conversation_to_feed * 2 + 1)
    context = message[prev:]
    for msg in context:
        req_message.append({
            "role": msg["role"],
            "content": msg["content"][0]["text"]
        })
    query = context[-1]["content"][0]["text"]
    # delete the last message from the req_message
    req_message.pop()
    context = similarity_search(query)
    if context:
        req_message.append({
            "role": ROLE,
            "content": info_context.format(
                context=similarity_search(query)
            )
        })
    req_message.append({
        "role": "user",
        "content": user_prompt.format(
            query=query
        )
    })

    return req_message


def phi3(message, max_tokens=1024, temperature=0.7, top_p=1):
    allowSelfSignedHttps(True)
    print(Config.PHI3_LOCATION)
    messages = format_message(message)

    if Config.PHI3_LOCATION == 'local' or Config.PHI3_LOCATION == 'port':
        url = "http://localhost:11434/api/chat/"
        # if Config.PHI3_LOCATION == 'port':
        #     url = "https://jj8bzvnc-11434.inc1.devtunnels.ms/api/chat/"
        data = {
            "model": "phi3",
            "messages": messages,
            "stream": False
        }
        with open("./queries/req_message_to_phi3.json", "w") as f:
            json.dump(data, f, indent=4)

        try:
            body = json.dumps(data)
            req = requests.post(url, data=body)
            response = req.json()
            with open("./queries/resp_from_phi3.json", "w") as f:
                json.dump(response, f, indent=4)
            return response.get("message").get("content")
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    if Config.PHI3_LOCATION == 'azure':
        data = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
        with open("./queries/req_message_to_phi3.json", "w") as f:
            json.dump(data, f, indent=4)
        url = "https://Phi-3-medium-4k-instruct-lirgh-serverless.eastus2.inference.ai.azure.com/v1/chat/completions"
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
            with open("./queries/resp_from_phi3.json", "w") as f:
                json.dump(response, f, indent=4)
            return response.get("choices")[0].get("message").get("content")
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""
