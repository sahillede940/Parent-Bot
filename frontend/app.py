import streamlit as st
import requests
import json
# Define the server URL
server_url = "http://127.0.0.1:5000/api/message"  # Replace with your server's URL

# Function to get a response from the server
def get_bot_response(user_query):
    try:
        response = requests.post(server_url, json={"query": user_query})
        if response.status_code == 200:
            return response.json().get("response").get("choices")[0].get("message").get("content")
        else:
            return "Error: Could not get a response from the server."
    except Exception as e:
        return f"Error: {e}"

# Streamlit app layout
st.title("Chatbot UI")
st.write("Ask me anything!")

# Input for the user's query
user_input = st.text_input("You:", "")

# Button to submit the query
if st.button("Send"):
    if user_input:
        # Get the bot's response
        bot_response = get_bot_response(user_input)
        print(bot_response)
        st.write("Bot:", bot_response)
    else:
        st.write("Please enter a query.")
