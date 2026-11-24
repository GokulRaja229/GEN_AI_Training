import os
from dotenv import load_dotenv
load_dotenv()


PROVIDER = os.getenv("LLM_PROVIDER","openai")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT","You are a helpful assistant.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL","gpt-4o-mini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL","gemini-1.5-turbo")

ollama_base_url = os.getenv("ollama_base_url")
ollama_model = os.getenv("ollama_model")

SUPPORTED_PROVIDERS = ["openai", "gemini", "ollama"]
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant. Answer clearly and concisely. If you don't know the answer, say 'I don't know.'")
#system prompt is a message that sets the behavior of the AI model. It tells the model how to respond to user inputs. In this case, it instructs the model to be helpful, clear, and concise, and to admit when it doesn't know something.
def get_configuration_error() -> str | None:
    if PROVIDER not in SUPPORTED_PROVIDERS:
        return f"Unsupported provider: {PROVIDER}. Supported providers are: {', '.join(SUPPORTED_PROVIDERS)}"
    
    if PROVIDER == "openai" and not OPENAI_API_KEY:
        return "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
    
    if PROVIDER == "gemini" and not GEMINI_API_KEY:
        return "Gemini API key is not set. Please set the GEMINI_API_KEY environment variable."
    
    if PROVIDER == "ollama" and (not ollama_base_url or not ollama_model):
        return "Ollama configuration is incomplete. Please set the ollama_base_url and ollama_model environment variables."
    
    return None