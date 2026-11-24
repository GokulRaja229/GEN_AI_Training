conversation_history: list[dict] = []

def add_to_conversation_history(role: str, content: str) -> None: 
    conversation_history.append({"role": role, "content": content})

def get_conversation_history() -> list[dict]:
    return conversation_history

def clear_conversation_history() -> None:
    conversation_history.clear()
        