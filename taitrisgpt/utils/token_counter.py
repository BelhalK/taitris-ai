# import tiktoken

# TOKEN_COSTS = {
#     "meta-llama/Llama-2-7b-chat-hf": {"prompt": 0.06, "completion": 0.12},
#     "text-embedding-ada-002": {"prompt": 0.0004, "completion": 0.0},
# }


# def count_message_tokens(messages, model="gpt-3.5-turbo-0613"):
#     try:
#         encoding = tiktoken.encoding_for_model(model)
#     except KeyError:
#         print("Warning: model not found. Using cl100k_base encoding.")
#         encoding = tiktoken.get_encoding("cl100k_base")
#     if model in {
#         "meta-llama/Llama-2-7b-chat-hf"
#         }:
#         tokens_per_message = 3
#         tokens_per_name = 1
#     else:
#         raise NotImplementedError(
#             f"""num_tokens_from_messages() is not implemented for model {model}."""
#         )
#     num_tokens = 0
#     for message in messages:
#         num_tokens += tokens_per_message
#         for key, value in message.items():
#             num_tokens += len(encoding.encode(value))
#             if key == "name":
#                 num_tokens += tokens_per_name
#     num_tokens += 3
#     return num_tokens


# def count_string_tokens(string: str, model_name: str) -> int:
#     encoding = tiktoken.encoding_for_model(model_name)
#     return len(encoding.encode(string))

TOKEN_MAX = {
    "gpt-3.5-turbo": 4096,
    "meta-llama/Llama-2-7b-chat-hf": 8192,
    "text-embedding-ada-002": 8192,
    "TinyPixel/Llama-2-7B-bf16-sharded": 8192
}

TOKEN_COSTS = {
    "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    "meta-llama/Llama-2-7b-chat-hf": {"prompt": 0.06, "completion": 0.12},
    "text-embedding-ada-002": {"prompt": 0.0004, "completion": 0.0},
    "TinyPixel/Llama-2-7B-bf16-sharded": {"prompt": 0.06, "completion": 0.12},
}


# def count_message_tokens(messages, model="gpt-3.5-turbo"):
#     if model in {
#         "gpt-3.5-turbo",
#         "meta-llama/Llama-2-7b-chat-hf",
#         "text-embedding-ada-002",
#         "TinyPixel/Llama-2-7B-bf16-sharded",
#     }:
#         tokens_per_message = 3
#         tokens_per_name = 1
#     elif model == "gpt-3.5-turbo-0301":
#         tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
#         tokens_per_name = -1  # if there's a name, the role is omitted
#     elif "gpt-3.5-turbo" in model:
#         print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
#         return count_message_tokens(messages, model="gpt-3.5-turbo")
#     elif "gpt-4" in model:
#         print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
#         return count_message_tokens(messages, model="gpt-4-0613")
#     else:
#         raise NotImplementedError(
#             f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
#         )
#     num_tokens = 0
#     for message in messages:
#         num_tokens += tokens_per_message
#         for key, value in message.items():
#             num_tokens += len(encoding.encode(value))
#             if key == "name":
#                 num_tokens += tokens_per_name
#     num_tokens += 3  
#     return num_tokens

def count_message_tokens(messages, model="gpt-3.5-turbo-0613"):
    return 10


def count_string_tokens(string: str, model_name: str) -> int:
    return 10
