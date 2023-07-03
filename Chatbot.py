import os
import openai
import requests
import streamlit as st

# Function to query the APIs
def query(api_url, payload):
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Fetch the API URLs from environment variables
api_urls = [
    os.environ.get('API_URL_1'),
    os.environ.get('API_URL_2'),
    os.environ.get('API_URL_3'),
    os.environ.get('API_URL_4'),
    os.environ.get('API_URL_5'),
    os.environ.get('API_URL_6'),
    os.environ.get('API_URL_7'),
]

# Streamlit Interface
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("FTWR")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Feed my Frankestein"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Query multiple APIs
    outputs = []
    for index, api_url in enumerate(api_urls, start=1):
        if api_url:
            output = query(api_url, {"question": prompt})
            if output:
                outputs.append(f"PC{index}: {output}")

    # Concatenate outputs to be sent to OpenAI
    fused_output = ' '.join(outputs)

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Send concatenated outputs to OpenAI model
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages + [{"role": "system", "content": fused_output}])
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
