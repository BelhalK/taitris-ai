from taitriscore.config import CONFIG

if CONFIG.platform == 'OPENAI':
    from taitriscore.basebot.openai_api import OpenAIAPI
elif CONFIG.platform == 'LLAMA':
    from taitriscore.basebot.hf_api import LLAMAAPI
elif CONFIG.platform == 'ANTHROPIC':
    from taitriscore.basebot.anthropic_api import AnthropicAPI
else:
    raise ValueError(f"Unsupported platform type: {CONFIG.platform}")

