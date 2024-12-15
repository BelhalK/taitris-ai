import tiktoken

TOKEN_MAX = {
    "gpt-3.5-turbo": 4096,
    "meta-llama/Llama-2-7b-chat-hf": 8192,
    "text-embedding-ada-002": 8192,
    "TinyPixel/Llama-2-7B-bf16-sharded": 8192,
}

TOKEN_COSTS = {
    "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    "meta-llama/Llama-2-7b-chat-hf": {"prompt": 0.06, "completion": 0.12},
    "text-embedding-ada-002": {"prompt": 0.0004, "completion": 0.0},
    "TinyPixel/Llama-2-7B-bf16-sharded": {"prompt": 0.06, "completion": 0.12},
}

def _safe_encode(text, encoding):
    """Safely encode text, converting any input to a string first."""
    try:
        if not isinstance(text, str):
            text = str(text)
        return encoding.encode(text)
    except Exception as e:
        print(f"Warning: Error encoding text: {e}")
        return []

def count_message_tokens(messages, model="gpt-3.5-turbo-0613"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model in {
        "meta-llama/Llama-2-7b-chat-hf"
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        tokens_per_message = 3
        tokens_per_name = 1
        print(f"Warning: model {model} not found. Using default values.")
    
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        if isinstance(message, dict):
            for key, value in message.items():
                num_tokens += len(_safe_encode(value, encoding))
                if key == "name":
                    num_tokens += tokens_per_name
        else:
            num_tokens += len(_safe_encode(message, encoding))
    num_tokens += 3
    return num_tokens

def count_string_tokens(string: str, model_name: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        return len(_safe_encode(string, encoding))
    except Exception as e:
        print(f"Warning: Error counting tokens: {e}")
        return 0

