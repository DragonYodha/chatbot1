import streamlit as st
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage

# pip install -qU langchain-ollama
# pip install langchain
# pip install streamlit

st.title("🧠 Make Your Own Chat Application with Ollama and Langchain!!!")
st.write("chatbot by VK")

# Sidebar for model selection
model_name = st.sidebar.selectbox(
    "Select Ollama Model",
    ["llama2","llama3.1:8b", "mistral", "gemma", "phi"],
    index=1
)

st.sidebar.info(f"""
If you get a 'model not found' error, run this command in your terminal:
```
ollama pull {model_name}
```
""")

with st.form("llm-form"):
    text = st.text_area("Enter your question or statement:")
    submit = st.form_submit_button("Submit")

def generate_response(input_text, model_name="llama2"):
    model = ChatOllama(model=model_name, base_url="http://localhost:11434")
    # Create a human message
    human_message = HumanMessage(content=input_text)
    # Get the response
    response = model.invoke([human_message])
    return response.content

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

if submit and text:
    with st.spinner(f"Generating response using {model_name}..."):
        try:
            response = generate_response(text, model_name)
            st.session_state['chat_history'].append({"user": text, "ollama": response})
        except Exception as e:
            st.error(f"Error generating response: {e}")
            response = f"Error: {e}"
            
            if "model not found" in str(e).lower():
                st.error(f"Please run 'ollama pull {model_name}' in your terminal to download the model.")

# Display chat history
st.write("## Chat History")
for chat in reversed(st.session_state['chat_history']):
    st.write(f"**🧑 User**: {chat['user']}")
    st.write(f"**🧠 Assistant**: {chat['ollama']}")
    st.write("---")