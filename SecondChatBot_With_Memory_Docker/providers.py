
import config
import requests
from google import genai
from openai import OpenAI


# -----------------------------
# OPENAI
# -----------------------------
def ask_openai(messages:list[dict]) -> str:  # message: list[dict] tells that message is a list of dictionaries, and the function returns a string.
    if not config.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set. Please set it in the .env file.")
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    try:
        response =client.chat.completions.create(
            model=config.OPENAI_MODEL,
           # instructions=config.SYSTEM_PROMPT,
            messages=messages
        )
    except Exception as e:
        raise RuntimeError(f"Error while calling OpenAI API: {e}")
    
    return response.choices[0].message.content if response.choices else "No response from OpenAI."


# -----------------------------
# GEMINI different approach
# -----------------------------
def ask_gemini(messages:list[dict]) -> str:  # message: list[dict] tells that message is a list of dictionaries, and the function returns a string.
    if not config.GEMINI_API_KEY:
        raise ValueError("Gemini API key is not set. Please set it in the .env file.")

    system_instruction=""
    contents=[]
    for message in messages:
        if message["role"]=="system":
            system_instruction=message["content"]
        else:
            gemini_role = "model" if message["role"] == "assistant" else "user"
            contents.append({"role": gemini_role,"parts":[message["content"]]})
#role is a string that indicates the role of the message sender. It can be either "user" or "assistant" or "system". The role helps the model understand the context of the conversation and generate appropriate responses. The "system" role is used for system-level instructions or messages that are not part of the user-assistant interaction.
#contents is a list of dictionaries that contains the messages exchanged between the user and the assistant. Each dictionary has a "role" key that indicates the role of the message sender, and a "parts" key that contains a list of message parts. The "parts" key allows for multi-part messages, where each part can be a separate piece of content. This structure helps the model understand the flow of the conversation and generate coherent responses.
    generation_settings = None
    if system_instruction:
        generation_settings = {
            "system_instruction": system_instruction
        }        

    client = genai.Client(
        api_key=config.GEMINI_API_KEY
    )
    try:
        response = client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=contents,
                config=generation_settings
            )
    except Exception as e:
        raise RuntimeError(f"Error while calling Gemini API: {e}")      

    return response.text


# -----------------------------
# OLLAMA
# -----------------------------
def ask_ollama(messages:list[dict]) -> str:  # message: list[dict] tells that message is a list of dictionaries, and the function returns a string.
    if not config.ollama_base_url or not config.ollama_model:
        raise ValueError("Ollama base URL or model is not set. Please set them in the .env file.")

    url = f"{config.ollama_base_url}/api/chat"

    payload = {
        "model": config.ollama_model,
        "messages": [
            {
                "role": "system",
                "content": config.SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": messages
            }
        ],
        "stream": False #whole response or one by one word, if True, then one by one word, if False, then whole response
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        

    except Exception as e:
        raise RuntimeError(f"Error while calling Ollama API: {e}")    

    result = response.json()

    return result["message"]["content"]
