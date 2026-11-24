import config
import memory
import streamlit as st
from providers import ask_openai, ask_gemini, ask_ollama

EXIT_COMMANDS = ["exit", "quit", "bye"]
def model_name():#getter model name based on the provider
    if config.PROVIDER == "openai":
        return config.OPENAI_MODEL
    elif config.PROVIDER == "gemini":
        return config.GEMINI_MODEL
    elif config.PROVIDER == "ollama":
        return config.ollama_model
    else:
        return "Unknown Model"

def check_setup():#checks if the setup is correct based on the provider and returns an error message if there's an issue, otherwise returns None.
    if config.PROVIDER == "openai":
        if not config.OPENAI_API_KEY:
            return "OpenAI API key is not set. Please set it in the .env file."
    elif config.PROVIDER == "gemini" and not config.GEMINI_API_KEY:
        return "Gemini API key is not set. Please set it in the .env file."
    elif config.PROVIDER == "ollama":
        if not config.ollama_base_url or not config.ollama_model:
            return "Ollama base URL or model is not set. Please set them in the .env file."
    else:
        return "Invalid provider specified in the .env file."
    
    return None  # No issues found    


def ask_llm(message:list[dict])-> str:#message:list[dict] tells that message is a list of dictionaries, and the function returns a string.
    if config.PROVIDER == "openai":
        return ask_openai(message)
    elif config.PROVIDER == "gemini":
        return ask_gemini(message)
    elif config.PROVIDER == "ollama":
        return ask_ollama(message)
    else:
        raise RuntimeError(f"Unsupported provider: {config.PROVIDER}. Supported providers are: {', '.join(config.SUPPORTED_PROVIDERS)}")

def build_message(history: list[dict], user_input: str) -> list[dict]:
    # Build the message list with system prompt, conversation history, and user input
    messages = [
        {"role": "system", "content": config.SYSTEM_PROMPT}
    ]
    
    # Add conversation history
    messages.extend(history)
    
    # Add the new user input
    messages.append({"role": "user", "content": user_input})
    
    return messages

st.set_page_config(page_title="Second ChatBot with Memory", page_icon="🤖")
st.title("Second ChatBot with Memory")
st.write("This is a chatbot that can remember the conversation history. It supports multiple LLM providers: OpenAI, Gemini, and Ollama.")

if "messages" not in st.session_state:
    st.session_state.messages = []

configuration_error = config.get_configuration_error()

if configuration_error:
    st.error(configuration_error)
    st.stop()

st.caption(f"Using provider: {config.PROVIDER}, Model: {config.OPENAI_MODEL if config.PROVIDER == 'openai' else config.GEMINI_MODEL if config.PROVIDER == 'gemini' else config.ollama_model}")

if st.button("Clear Conversation History"):
    memory.clear_conversation_history()
    st.session_state.messages = []
    st.success("Conversation history cleared.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    #messages = build_message(st.session_state.messages, user_input)
    history = memory.get_conversation_history()

    messages = build_message(history, user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    memory.add_to_conversation_history("user", user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    
    try:
        response = ask_llm(messages)
        
        memory.add_to_conversation_history("assistant", response)       
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    except Exception as e:
        st.error(f"Error: {e}")




def main():
    setup_issue = check_setup()
    if setup_issue:
        print(setup_issue)
        return

    print(f"Using provider: {config.PROVIDER}")
    print(f"Model: {model_name()}")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in EXIT_COMMANDS:
            break
        
        try:
            response = ask_llm(build_message(memory.get_conversation_history(), user_input))
            # Add the user input and model response to the conversation history
            memory.add_to_conversation_history("user", user_input)
            memory.add_to_conversation_history("assistant", response)
            print(f"{config.PROVIDER.capitalize()} Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

#if __name__ == "__main__":
    #main()    