import json
import requests
import streamlit as st
from streamlit_chat import message


def handle_llm_request(conversation):
    llm_response = requests.get(f'https://dd9d-2604-3d08-937f-1360-847c-215-6d83-d627.ngrok-free.app/ask?question={conversation}')
    llm_response = llm_response.json()

    return llm_response['output']


def generate_streamlit_payload(content, type):
    payload = {
        "type": type,
        "content": content
    }

    return payload

def LLM_format_data(messages):
    llm_input = []
    for message in messages:
        if message['type'] == 'user':
            llm_input.append(f"USER: {message['content']}")
        if message['type'] == 'AI':
            llm_input.append(f"ASSISTANT: {message['content']}")

    llm_input = '\n'.join(llm_input)
    return llm_input
def main():
    st.header("Your own ChatGPT 🤖")

    if user_query := st.chat_input('talk to an AI'):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.session_state.messages.append(generate_streamlit_payload(user_query, "user"))

        llm_input_data = LLM_format_data(st.session_state.messages)
        print(llm_input_data)
        response = handle_llm_request(llm_input_data)

        st.session_state.messages.append(generate_streamlit_payload(response, 'AI'))

        # this just renders it
        for message in st.session_state.messages:
            with st.chat_message(message["type"]):
                st.markdown(message['content'])


if __name__ == '__main__':
    main()
