import streamlit as st
import os
from groq import Groq
from typing import Generator
from home import check_session

if not check_session():
    st.switch_page('home.py')

# Show title and description.
st.title("AI Assistant")
st.write(
    "This is a chatbot running Meta's LLaMA 3.1 70b model. Ask it anything. "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
groq_api_key = "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"
os.environ["GROQ_API_KEY"] = groq_api_key
# Create an OpenAI client.
client = Groq()

#TODO: WHAT THE FRICK IS RAW TEXT????
initial_prompt = {
    "role": "system",
    "content": "Read this information and answer questions related: "+open("rawtext.txt").read()
}

if "messages" not in st.session_state:
    st.session_state.messages = [initial_prompt]

def generateResponse(completion) -> Generator[str, None, None]:
    for data in completion:
        if data.choices[0].delta.content:
            yield data.choices[0].delta.content
    

for message in st.session_state.messages:
    if(message["role"]!="system"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role":"user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role" : m["role"],
                "content" : m["content"]
            }
            for m in st.session_state.messages
        ],
        max_tokens=4000,
        stream = True
    )

    with st.chat_message("assistant"):
        generator = generateResponse(completion)
        response = st.write_stream(generator)
    if isinstance(response, str):
        st.session_state.messages.append({"role": "assistant", "content":response})
    else:
        combined = "\n".join(str(item) for item in response)
        st.session_state.messages.append({"role":"assistant", "content":combined})
